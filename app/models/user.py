from datetime import date

from black import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, func, TIMESTAMP

from app.entities.user import UserEntity
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True)
    name: str = Column(String(100), nullable=False)
    birth_date: date = Column(Date, nullable=True)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=True)

    created_at: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: datetime = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            name=self.name,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            birth_date=self.birth_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: UserEntity) -> "User":
        return User(
            id=user.id,
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            birth_date=user.birth_date,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
