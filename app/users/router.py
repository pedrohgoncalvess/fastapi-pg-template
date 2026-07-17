from fastapi import Depends, APIRouter
from starlette import status

from app.auth.models import UserCreate, UserUpdate
from app.auth.services import get_current_user
from app.users.services import register_user, update_user_info
from database.models.base import User


router = APIRouter(
    prefix="/users",
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    new_user = await register_user(user)
    return {
        "name": new_user.name,
        "email": new_user.email,
    }


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "name": user.name,
        "email": user.email,
    }


@router.patch("/me")
async def update_me(payload: UserUpdate, user: User = Depends(get_current_user)):
    updated_user = await update_user_info(user, payload)
    return {
        "name": updated_user.name,
        "email": updated_user.email,
    }
