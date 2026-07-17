import uuid
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from passlib.context import CryptContext

from app.auth.models import TokenData, UserLogin, RefreshTokenRequest
from app.exceptions import (
    InvalidCredentials,
    UserNotVerified,
    InvalidRefreshToken,
    RefreshTokenExpired,
)
from database.connection import DatabaseConnection
from database.models.base import User, Refresh
from database.operations.base import RefreshRepository
from database.operations.base.user import UserRepository
from utils import get_env_var


SECRET_KEY = get_env_var("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90
REFRESH_TOKEN_EXPIRE_MINUTES = 300
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    async with DatabaseConnection().session() as session:
        user_repository = UserRepository(session)

        try:
            token = credentials.credentials
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.exceptions.PyJWTError:
            raise credentials_exception

        user = await user_repository.find_by_email(email)
        if user is None or user.deleted_at is not None:
            raise credentials_exception

        return user


def _token_response(access_token: str, refresh_token: str) -> dict:
    access_token_expires_at = (datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).strftime("%Y-%m-%d %H:%M:%S")
    refresh_token_expires_at = (datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "access_token": {"token": access_token, "expires": access_token_expires_at},
        "refresh_token": {"token": refresh_token, "expires": refresh_token_expires_at},
        "token_type": "bearer",
    }


def _create_access_token_for(user: User) -> str:
    return create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


async def login_user(user_auth: UserLogin) -> dict:
    async with DatabaseConnection().session() as session:
        user_repository = UserRepository(session)
        refresh_repository = RefreshRepository(session)

        user = await user_repository.find_by_email(user_auth.email)
        if user is None or not verify_password(user_auth.password, user.password):
            raise InvalidCredentials()

        if not user.is_verified:
            raise UserNotVerified()

        refresh_token = str(uuid.uuid4())
        await refresh_repository.insert(
            Refresh(
                token=refresh_token,
                user_id=user.id,
            )
        )

        return _token_response(_create_access_token_for(user), refresh_token)


async def refresh_access_token(payload: RefreshTokenRequest) -> dict:
    async with DatabaseConnection().session() as session:
        refresh_repository = RefreshRepository(session)
        user_repository = UserRepository(session)

        refresh = await refresh_repository.find_by_token(payload.refresh_token)
        if not refresh:
            raise InvalidRefreshToken()

        user = await user_repository.find_by_id(refresh.user_id)

        if refresh.inserted_at + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES) < datetime.utcnow() or refresh.used:
            raise RefreshTokenExpired()

        await refresh_repository.update(refresh.id, {"used": True})

        new_refresh_token = str(uuid.uuid4())
        await refresh_repository.insert(
            Refresh(
                token=new_refresh_token,
                user_id=user.id,
            )
        )

        return _token_response(_create_access_token_for(user), new_refresh_token)
