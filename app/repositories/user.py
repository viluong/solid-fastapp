from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing_extensions import Optional

from app.entities.user import UserEntity
from app.models.user import User
from app.repositories.base import BaseRepository


class IUserRepository(BaseRepository):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass


class UserRepository(IUserRepository, ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_entity: UserEntity) -> UserEntity:
        user = User.from_entity(user_entity)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user.to_entity()

    async def get(self, id: int) -> Optional[UserEntity]:
        result = await self.session.execute(select(User).where(User.id == id))
        user: User = result.scalars().first()
        return user.to_entity() if user else None

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self.session.execute(select(User).where(User.email == email))
        user: User = result.scalars().first()
        if not user:
            return None
        return user.to_entity()
