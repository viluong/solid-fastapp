from abc import abstractmethod, ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Optional

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate


class IUserRepository(BaseRepository):
    @abstractmethod
    async def get_by_email(self, email: str):
        pass


class UserRepository(IUserRepository, ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        new_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            name=user.name,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get(self, id: int) -> Optional[User]:
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
