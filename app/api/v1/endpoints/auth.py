from fastapi import APIRouter, Depends

from app.dependencies import get_auth_service
from app.schemas.token import TokenResponse, UserLogin
from app.services.auth import IAuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin, service: IAuthService = Depends(get_auth_service)
):
    return await service.login_with_email(user_login)
