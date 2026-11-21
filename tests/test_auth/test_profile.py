import pytest
from httpx import AsyncClient


async def get_token(client: AsyncClient):
    """Helper to get a valid token."""
    await client.post(
        "/auth/register",
        json={
            "username": "me_tester",
            "email": "me@test.com",
            "name": "Me",
            "last_name": "Tester",
            "password": "pass1234",
        },
    )
    res = await client.post(
        "/auth/login", data={"username": "me_tester", "password": "pass1234"}
    )
    return res.json()["access_token"]


@pytest.mark.asyncio
async def test_get_me_with_valid_token(client: AsyncClient):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "me_tester"


@pytest.mark.asyncio
async def test_get_me_without_token(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401
