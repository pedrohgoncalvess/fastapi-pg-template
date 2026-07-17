from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from app.auth.models import UserCreate, UserUpdate
from app.auth.services import get_current_user, verify_password
from app.users.services import get_password_hash
from database.connection import DatabaseConnection
from database.models.base import User
from database.operations.base.user import UserRepository


router = APIRouter(
    prefix="/users",
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    async with DatabaseConnection().session() as session:

        user_repository = UserRepository(session)
        exists = await user_repository.find_by_email(user.email)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        hashed_password = get_password_hash(user.password)
        new_user = User(
            email=user.email,
            name=user.name,
            password=hashed_password
        )
        _ = await user_repository.insert(new_user)

    return new_user.__dict__


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "name": user.name,
        "email": user.email
    }


@router.patch("/me")
async def update_me(payload: UserUpdate, user: User = Depends(get_current_user)):
    async with DatabaseConnection().session() as session:
        user_repository = UserRepository(session)
        update_data = {}

        if payload.new_password is not None:
            if payload.old_password is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="old_password is required to set a new password."
                )
            if not verify_password(payload.old_password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Old password incorrect."
                )
            update_data["password"] = get_password_hash(payload.new_password)

        if payload.email is not None and payload.email != user.email:
            exists = await user_repository.find_by_email(payload.email)
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered."
                )
            update_data["email"] = payload.email

        if payload.name is not None:
            update_data["name"] = payload.name

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update."
            )

        updated_user = await user_repository.update(user.id, update_data)

    return {
        "name": updated_user.name,
        "email": updated_user.email
    }
