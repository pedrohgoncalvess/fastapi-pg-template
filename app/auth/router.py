from fastapi import APIRouter

from app.auth.models import UserLogin, RefreshTokenRequest
from app.auth.services import login_user, refresh_access_token


router = APIRouter(
    prefix="/auth",
)


@router.post("")
async def login(user_auth: UserLogin):
    return await login_user(user_auth)


@router.post("/refresh")
async def refresh_token(payload: RefreshTokenRequest):
    return await refresh_access_token(payload)
