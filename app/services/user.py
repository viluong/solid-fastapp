from abc import ABC

from app.core.exceptions import DuplicateEmailException
from app.models.user import User
from app.repositories.user import IUserRepository
from app.schemas.user import UserCreate


class IUserService(ABC):

    async def create_user(self, user_create: UserCreate) -> User:
        pass


class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        user = await self.repository.get_by_email(user_create.email)
        if user:
            raise DuplicateEmailException
        new_user = await self.repository.create(user_create)
        return new_user
