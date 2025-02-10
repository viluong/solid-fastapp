from abc import ABC, abstractmethod
from typing import Optional

from app.core.exceptions import AuthenticationFailException
from app.core.security import verify_password, create_access_token
from app.entities.token import TokenEntity
from app.entities.user import UserEntity
from app.repositories.user import IUserRepository
from app.schemas.token import UserLogin


class IAuthService(ABC):

    @abstractmethod
    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def login_with_email(self, user_login: UserLogin) -> TokenEntity:
        pass


class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[UserEntity]:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def login_with_email(self, user_login: UserLogin) -> TokenEntity:
        user_entity: UserEntity = await self.authenticate_user(
            user_login.email, user_login.password
        )
        if not user_entity:
            raise AuthenticationFailException

        token = create_access_token({"id": user_entity.id, "email": user_entity.email})
        return TokenEntity(access_token=token, token_type="bearer")
