import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    payload = {
        "username": "test_user_1",
        "email": "test1@example.com",
        "name": "Test",
        "last_name": "User",
        "password": "SecurePass123!",
    }
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_user_1"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    # First register
    await client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "email": "d1@test.com",
            "name": "D",
            "last_name": "U",
            "password": "pass1234",
        },
    )
    # Second register with same username
    response = await client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "email": "d2@test.com",
            "name": "D",
            "last_name": "U",
            "password": "pass1234",
        },
    )
    assert response.status_code == 400
