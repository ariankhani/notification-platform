import pytest


@pytest.mark.asyncio
async def test_notification_rule_crud_and_filtering(
    client,
    authenticated_user_factory,
    event_and_role_factory,
    notification_rule_factory,
):
    headers, _ = await authenticated_user_factory()
    _, first_role = await event_and_role_factory()
    _, second_role = await event_and_role_factory()

    first_rule = await notification_rule_factory(
        headers,
        first_role.id,
        event_type="invoice.created",
    )
    second_rule = await notification_rule_factory(
        headers,
        second_role.id,
        event_type="user.created",
        channel="sms",
    )
    assert first_rule.status_code == 201, first_rule.text
    assert second_rule.status_code == 201, second_rule.text

    filtered = await client.get(
        "/notifications/rules?event_type=invoice.created",
        headers=headers,
    )
    assert filtered.status_code == 200
    assert all(rule["event_type"] == "invoice.created" for rule in filtered.json())

    rule_id = first_rule.json()["id"]
    updated = await client.patch(
        f"/notifications/rules/{rule_id}",
        headers=headers,
        json={"channel": "push", "is_active": False},
    )
    assert updated.status_code == 200
    assert updated.json()["channel"] == "push"
    assert updated.json()["is_active"] is False

    deleted = await client.delete(
        f"/notifications/rules/{rule_id}",
        headers=headers,
    )
    assert deleted.status_code == 204

    missing = await client.patch(
        f"/notifications/rules/{rule_id}",
        headers=headers,
        json={"is_active": True},
    )
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_notification_rule_is_rejected(
    client,
    authenticated_user_factory,
    event_and_role_factory,
    notification_rule_factory,
):
    headers, _ = await authenticated_user_factory()
    _, role = await event_and_role_factory()

    first_response = await notification_rule_factory(headers, role.id)
    duplicate_response = await notification_rule_factory(headers, role.id)

    assert first_response.status_code == 201, first_response.text
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"]


@pytest.mark.asyncio
async def test_rule_requires_existing_role(
    client,
    authenticated_user_factory,
    notification_rule_factory,
):
    headers, _ = await authenticated_user_factory()

    response = await notification_rule_factory(headers, 999_999)

    assert response.status_code == 400
    assert response.json()["detail"] == "Role not found"
