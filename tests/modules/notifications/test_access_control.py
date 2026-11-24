import pytest


@pytest.mark.asyncio
async def test_my_notifications_requires_authentication(client):
    response = await client.get("/notifications/my")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_rule_management_requires_authentication(client):
    response = await client.get("/notifications/rules")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_notification_requires_authentication(client):
    response = await client.post(
        "/notifications/",
        json={
            "event_id": 1,
            "user_id": 1,
            "channel": "email",
            "message": "Not authenticated",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_create_notification_for_another_user(
    client,
    authenticated_user_factory,
):
    headers, user_id = await authenticated_user_factory()

    response = await client.post(
        "/notifications/",
        headers=headers,
        json={
            "event_id": 1,
            "user_id": user_id + 1,
            "channel": "email",
            "message": "Not allowed",
        },
    )

    assert response.status_code == 403
