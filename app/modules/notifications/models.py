from datetime import UTC, datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class NotificationStatus(str, PyEnum):
    PENDING = "pending"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationRule(SQLModel, table=True):
    __tablename__ = "notification_rules"
    __table_args__ = (
        UniqueConstraint(
            "event_type",
            "role_id",
            "channel",
            name="uq_notification_rule_event_role_channel",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    event_type: str = Field(max_length=100, index=True)
    channel: str = Field(max_length=50)
    role_id: int = Field(foreign_key="roles.id")
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(default=None)

    notifications: list["Notification"] = Relationship(back_populates="rule")


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    rule_id: int | None = Field(default=None, foreign_key="notification_rules.id")
    
    channel: str = Field(max_length=50)
    message: str = Field(max_length=5000)
    status: NotificationStatus = Field(default=NotificationStatus.PENDING)
    
    rendered_content: dict | None = Field(default=None, sa_type=JSON)
    error_message: str | None = Field(default=None, max_length=1000)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sent_at: datetime | None = Field(default=None)

    user: "User" = Relationship(back_populates="notifications")
    rule: NotificationRule | None = Relationship(back_populates="notifications")
