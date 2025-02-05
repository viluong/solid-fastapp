from abc import abstractmethod, ABC

from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate


class IUserRepository(BaseRepository):
    @abstractmethod
    def get_by_email(self, email: str):
        pass


class UserRepository(IUserRepository, ABC):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> User:
        db_user = User(email=user.email, hashed_password=get_password_hash(user.password), name=user.name)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()