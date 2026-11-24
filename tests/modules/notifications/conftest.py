import uuid

import pytest

from app.models.event import Event
from app.models.role import Role


@pytest.fixture
def authenticated_user_factory(client):
    async def create_user():
        suffix = uuid.uuid4().hex
        username = f"notification-user-{suffix}"
        password = "Strong-test-password-123"
        register_response = await client.post(
            "/auth/register",
            json={
                "username": username,
                "email": f"{suffix}@example.com",
                "name": "Notification",
                "last_name": "Tester",
                "password": password,
            },
        )
        assert register_response.status_code == 201, register_response.text

        login_response = await client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200, login_response.text
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        return headers, register_response.json()["id"]

    return create_user


@pytest.fixture
def event_and_role_factory(db_session):
    async def create_domain_records():
        suffix = uuid.uuid4().hex
        event = Event(
            platform="test",
            event_type=f"invoice.created.{suffix}",
            message="An invoice was created",
        )
        role = Role(
            name=f"notification-role-{suffix}",
            description="Role created by notification tests",
        )
        db_session.add(event)
        db_session.add(role)
        await db_session.commit()
        await db_session.refresh(event)
        await db_session.refresh(role)
        return event, role

    return create_domain_records


@pytest.fixture
def notification_rule_factory(client):
    async def create_rule(headers, role_id, **overrides):
        payload = {
            "event_type": "invoice.created",
            "channel": "email",
            "role_id": role_id,
            "is_active": True,
        }
        payload.update(overrides)
        return await client.post(
            "/notifications/rules",
            headers=headers,
            json=payload,
        )

    return create_rule
