from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from app.auth.models import UserCreate
from app.auth.services import get_current_user
from app.users.services import get_password_hash
from database.connection import DatabaseConnection
from database.models.base import User
from database.operations.base.user import UserRepository


router = APIRouter(
    prefix="/users",
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    async with DatabaseConnection() as conn:

        user_repository = UserRepository(conn)
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