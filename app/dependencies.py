from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .repositories.user import IUserRepository, UserRepository
from .services.user import IUserService, UserService


def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)

def get_user_service(user_repo: IUserRepository = Depends(get_user_repository)) -> IUserService:
    return UserService(user_repo)