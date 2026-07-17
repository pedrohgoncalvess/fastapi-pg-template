from passlib.context import CryptContext

from app.auth.models import UserCreate, UserUpdate
from app.auth.services import verify_password
from app.exceptions import (
    EmailAlreadyRegistered,
    OldPasswordRequired,
    OldPasswordIncorrect,
    NothingToUpdate,
)
from database.connection import DatabaseConnection
from database.models.base import User
from database.operations.base.user import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def register_user(user: UserCreate) -> User:
    async with DatabaseConnection().session() as session:
        user_repository = UserRepository(session)

        if await user_repository.find_by_email(user.email):
            raise EmailAlreadyRegistered()

        new_user = User(
            email=user.email,
            name=user.name,
            password=get_password_hash(user.password),
        )
        await user_repository.insert(new_user)

    return new_user


async def update_user_info(user: User, payload: UserUpdate) -> User:
    async with DatabaseConnection().session() as session:
        user_repository = UserRepository(session)
        update_data = {}

        if payload.new_password is not None:
            if payload.old_password is None:
                raise OldPasswordRequired()
            if not verify_password(payload.old_password, user.password):
                raise OldPasswordIncorrect()
            update_data["password"] = get_password_hash(payload.new_password)

        if payload.email is not None and payload.email != user.email:
            if await user_repository.find_by_email(payload.email):
                raise EmailAlreadyRegistered()
            update_data["email"] = payload.email

        if payload.name is not None:
            update_data["name"] = payload.name

        if not update_data:
            raise NothingToUpdate()

        return await user_repository.update(user.id, update_data)
