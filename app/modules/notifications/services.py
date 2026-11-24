# app/modules/notifications/services.py
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.event import Event
from app.models.role import Role
from app.models.user import User

from .models import Notification, NotificationRule, NotificationStatus
from .schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationRuleCreate,
    NotificationRuleResponse,
    NotificationRuleUpdate,
)


async def create_notification(
    session: AsyncSession, data: NotificationCreate
) -> NotificationResponse:
    event = await session.get(Event, data.event_id)
    if event is None:
        raise ValueError("Event not found")

    user = await session.get(User, data.user_id)
    if user is None:
        raise ValueError("User not found")

    if data.rule_id is not None:
        stmt = select(NotificationRule).where(
            NotificationRule.id == data.rule_id,
            NotificationRule.is_active.is_(True),
        )
        result = await session.exec(stmt)
        rule = result.first()

        if not rule:
            raise ValueError("Notification rule is inactive or not found")
        if rule.channel != data.channel:
            raise ValueError("Notification channel does not match its rule")

    notification = Notification(
        event_id=data.event_id,
        user_id=data.user_id,
        rule_id=data.rule_id,
        channel=data.channel,
        message=data.message,
        status=NotificationStatus.PENDING,
    )

    session.add(notification)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Notification violates a database constraint") from exc
    await session.refresh(notification)

    return NotificationResponse.model_validate(notification)


async def get_user_notifications(
    session: AsyncSession, user_id: int, skip: int = 0, limit: int = 20
) -> list[NotificationResponse]:
    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc(), Notification.id.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await session.exec(stmt)
    return [NotificationResponse.model_validate(n) for n in result.all()]




async def create_notification_rule(
    session: AsyncSession, data: NotificationRuleCreate
) -> NotificationRuleResponse:

    role = await session.get(Role, data.role_id)
    if role is None:
        raise ValueError("Role not found")

    stmt = select(NotificationRule).where(
        NotificationRule.event_type == data.event_type,
        NotificationRule.role_id == data.role_id,
        NotificationRule.channel == data.channel,
    )
    result = await session.exec(stmt)
    if result.first():
        raise ValueError("A rule with this event_type, role and channel already exists")

    rule = NotificationRule(
        event_type=data.event_type,
        channel=data.channel,
        role_id=data.role_id,
        is_active=data.is_active,
    )

    session.add(rule)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError(
            "A rule with this event_type, role and channel already exists"
        ) from exc
    await session.refresh(rule)

    return NotificationRuleResponse.model_validate(rule)


async def list_notification_rules(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    event_type: str | None = None,
) -> list[NotificationRuleResponse]:
    stmt = select(NotificationRule).order_by(NotificationRule.id).offset(skip).limit(limit)

    if event_type:
        stmt = stmt.where(NotificationRule.event_type == event_type)

    result = await session.exec(stmt)
    return [NotificationRuleResponse.model_validate(r) for r in result.all()]


async def update_notification_rule(
    session: AsyncSession, rule_id: int, data: NotificationRuleUpdate
) -> NotificationRuleResponse:
    stmt = select(NotificationRule).where(NotificationRule.id == rule_id)
    result = await session.exec(stmt)
    rule = result.first()

    if not rule:
        raise ValueError("Notification rule not found")

    update_data = data.model_dump(exclude_unset=True)
    if "role_id" in update_data:
        role = await session.get(Role, update_data["role_id"])
        if role is None:
            raise ValueError("Role not found")
    for field, value in update_data.items():
        setattr(rule, field, value)

    session.add(rule)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError(
            "A rule with this event_type, role and channel already exists"
        ) from exc
    await session.refresh(rule)

    return NotificationRuleResponse.model_validate(rule)


async def delete_notification_rule(session: AsyncSession, rule_id: int) -> bool:
    stmt = select(NotificationRule).where(NotificationRule.id == rule_id)
    result = await session.exec(stmt)
    rule = result.first()

    if not rule:
        return False

    await session.delete(rule)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Rule is referenced by existing notifications") from exc
    return True
