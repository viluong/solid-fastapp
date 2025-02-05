from abc import ABC
from typing import Optional

from app.core.exceptions import DuplicateEmailException
from app.models.user import User
from app.repositories.user import IUserRepository
from app.schemas.user import UserCreate

class IUserService(ABC):

    def create_user(self, user_create: UserCreate) -> User:
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        pass

class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(self, user_create: UserCreate) -> User:
        if self.repository.get_by_email(user_create.email):
            raise DuplicateEmailException
        user = self.repository.create(user_create)
        return user
