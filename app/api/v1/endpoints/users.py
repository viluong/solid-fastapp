from fastapi import APIRouter, Depends

from app.dependencies import get_user_service
from app.schemas.user import UserResponse, UserCreate
from app.services.user import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_create: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_create)
