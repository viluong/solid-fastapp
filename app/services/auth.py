from typing import Optional

from app.core.security import verify_password
from app.models.user import User
from app.repositories.user import IUserRepository


class AuthService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user