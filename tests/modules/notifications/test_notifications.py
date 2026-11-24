import pytest


@pytest.mark.asyncio
async def test_authenticated_user_can_list_own_notifications(
    client,
    authenticated_user_factory,
):
    headers, _ = await authenticated_user_factory()

    response = await client.get("/notifications/my", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_notification_success(
    client,
    authenticated_user_factory,
    event_and_role_factory,
):
    headers, user_id = await authenticated_user_factory()
    event, _ = await event_and_role_factory()

    response = await client.post(
        "/notifications/",
        headers=headers,
        json={
            "event_id": event.id,
            "user_id": user_id,
            "channel": "email",
            "message": "Invoice created",
        },
    )

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["event_id"] == event.id
    assert body["user_id"] == user_id
    assert body["channel"] == "email"
    assert body["status"] == "pending"


@pytest.mark.asyncio
async def test_create_notification_rejects_unknown_event(
    client,
    authenticated_user_factory,
):
    headers, user_id = await authenticated_user_factory()

    response = await client.post(
        "/notifications/",
        headers=headers,
        json={
            "event_id": 999_999,
            "user_id": user_id,
            "channel": "email",
            "message": "Unknown event",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Event not found"


@pytest.mark.asyncio
async def test_notification_rule_channel_must_match(
    client,
    authenticated_user_factory,
    event_and_role_factory,
    notification_rule_factory,
):
    headers, user_id = await authenticated_user_factory()
    event, role = await event_and_role_factory()
    rule_response = await notification_rule_factory(headers, role.id)
    assert rule_response.status_code == 201, rule_response.text

    response = await client.post(
        "/notifications/",
        headers=headers,
        json={
            "event_id": event.id,
            "user_id": user_id,
            "rule_id": rule_response.json()["id"],
            "channel": "sms",
            "message": "Wrong channel",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Notification channel does not match its rule"


@pytest.mark.asyncio
async def test_inactive_notification_rule_is_rejected(
    client,
    authenticated_user_factory,
    event_and_role_factory,
    notification_rule_factory,
):
    headers, user_id = await authenticated_user_factory()
    event, role = await event_and_role_factory()
    rule_response = await notification_rule_factory(
        headers,
        role.id,
        is_active=False,
    )
    assert rule_response.status_code == 201, rule_response.text

    response = await client.post(
        "/notifications/",
        headers=headers,
        json={
            "event_id": event.id,
            "user_id": user_id,
            "rule_id": rule_response.json()["id"],
            "channel": "email",
            "message": "Inactive rule",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Notification rule is inactive or not found"


@pytest.mark.asyncio
async def test_notifications_are_isolated_and_paginated(
    client,
    authenticated_user_factory,
    event_and_role_factory,
):
    first_headers, first_user_id = await authenticated_user_factory()
    second_headers, second_user_id = await authenticated_user_factory()
    event, _ = await event_and_role_factory()

    for message in ("First", "Second"):
        response = await client.post(
            "/notifications/",
            headers=first_headers,
            json={
                "event_id": event.id,
                "user_id": first_user_id,
                "channel": "email",
                "message": message,
            },
        )
        assert response.status_code == 201, response.text

    second_user_response = await client.get(
        "/notifications/my",
        headers=second_headers,
    )
    paginated_response = await client.get(
        "/notifications/my?skip=0&limit=1",
        headers=first_headers,
    )

    assert second_user_id != first_user_id
    assert second_user_response.status_code == 200
    assert second_user_response.json() == []
    assert paginated_response.status_code == 200
    assert len(paginated_response.json()) == 1
    assert paginated_response.json()[0]["message"] == "Second"
