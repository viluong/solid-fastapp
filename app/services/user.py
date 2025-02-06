from abc import ABC, abstractmethod

from app.core.exceptions import DuplicateEmailException
from app.core.security import get_password_hash
from app.entities.user import UserEntity
from app.repositories.user import IUserRepository
from app.schemas.user import UserCreate


class IUserService(ABC):

    @abstractmethod
    async def create_user(self, user_create: UserCreate) -> UserEntity:
        pass


class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> UserEntity:
        user: UserEntity = await self.repository.get_by_email(user_create.email)
        if user:
            raise DuplicateEmailException

        new_user: UserEntity = UserEntity(
            email=user_create.email,
            name=user_create.name,
            birth_date=user_create.birth_date,
            hashed_password=get_password_hash(user_create.password),
        )

        new_user: UserEntity = await self.repository.create(new_user)
        return new_user
