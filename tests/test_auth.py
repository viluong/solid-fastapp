from datetime import date, datetime

import pytest

from app.entities.user import UserEntity
from app.repositories.user import UserRepository


async def mock_create_fake_user(self, user_entity: UserEntity):
    return UserEntity(
        id=1,
        email="viluong12@yopmail.com",
        name="Vi Luong",
        birth_date=date(1994, 10, 10),
        hashed_password="$2b$12$jGnCBXEAm8UO41ru89/iQefprqErhQ/Mhf5pDXqBssuW11t07xeOG",
        is_active=True,
        updated_at=datetime(2024, 1, 1, 1, 1, 1),
        created_at=datetime(2024, 1, 1, 1, 1, 1),
    )


async def mock_user_none(self, email: str):
    return None


@pytest.mark.asyncio
async def test_register_user(async_client, monkeypatch):

    monkeypatch.setattr(UserRepository, "get_by_email", mock_user_none)
    monkeypatch.setattr(UserRepository, "create", mock_create_fake_user)
    user_data = {
        "email": "viluong12@yopmail.com",
        "password": "12345678",
        "name": "Vi Luong",
        "birth_date": "10/10/1994",
    }
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "viluong12@yopmail.com"


@pytest.mark.asyncio
async def test_login_user(async_client, monkeypatch):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_user_none)
    monkeypatch.setattr(UserRepository, "create", mock_create_fake_user)

    user_data = {
        "email": "viluong1234@yopmail.com",
        "password": "12345678",
        "name": "Vi Luong",
        "birth_date": "10/10/1994",
    }
    await async_client.post("/api/v1/auth/register", json=user_data)
    monkeypatch.setattr(UserRepository, "get_by_email", mock_create_fake_user)

    login_data = {"email": "viluong1234@yopmail.com", "password": "12345678"}
    response = await async_client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(async_client, monkeypatch):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_user_none)

    login_data = {"email": "viluong1@yopmail.com", "password": "wrongpassword"}
    response = await async_client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Authentication failed. Please check your credentials."
