import pytest
from httpx import AsyncClient


@pytest.fixture
async def registered_user(client: AsyncClient):
    """Fixture to create a user before login tests."""
    payload = {
        "username": "login_tester",
        "email": "login@test.com",
        "name": "Login",
        "last_name": "Tester",
        "password": "pass1234",
    }
    await client.post("/auth/register", json=payload)
    return payload


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, registered_user):
    response = await client.post(
        "/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, registered_user):
    response = await client.post(
        "/auth/login",
        data={"username": registered_user["username"], "password": "wrong_password"},
    )
    assert response.status_code == 401
