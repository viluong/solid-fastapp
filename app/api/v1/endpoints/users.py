from fastapi import APIRouter, Depends, HTTPException

from app.core.exceptions import DuplicateEmailException
from app.dependencies import get_user_service
from app.schemas.user import UserResponse, UserCreate
from app.services.user import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user_create: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user_create)
    except DuplicateEmailException as e:
        raise HTTPException(status_code=400, detail="Email already registered")
