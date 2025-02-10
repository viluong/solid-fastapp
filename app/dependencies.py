from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .repositories.user import IUserRepository, UserRepository
from .services.auth import IAuthService, AuthService
from .services.user import IUserService, UserService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)


def get_user_service(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> IUserService:
    return UserService(user_repo)


def get_auth_service(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> IAuthService:
    return AuthService(user_repo)
