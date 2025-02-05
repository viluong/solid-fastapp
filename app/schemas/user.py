from datetime import datetime, date

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    birth_date: date

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birthdate(cls, value):
        try:
            birthdate_obj = datetime.strptime(value, "%m/%d/%Y").date()
            if birthdate_obj >= date.today():
                raise ValueError("birth_date cannot be in the future")
            return birthdate_obj
        except ValueError:
            raise ValueError("birth_date must be in MM/DD/YYYY format")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    age: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
