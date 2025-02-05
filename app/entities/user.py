from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class UserEntity:
    id: Optional[int] = None
    email: Optional[str] = None
    name: Optional[str] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None
    birth_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
