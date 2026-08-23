from datetime import datetime

from sqlmodel import Field

from app.schemas.notification import (
    NotificationBase,
    NotificationRuleBase,
    NotificationStatus,
)


class NotificationRule(NotificationRuleBase, table=True):
    """
    قلب تصمیم‌گیری: مشخص می‌کند وقتی یک event با event_type مشخص می‌رسد،
    کدام role باید نوتیفای شود و از چه channel ای.
    """

    __tablename__ = "notification_rules"

    id: int | None = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="roles.id")


class Notification(NotificationBase, table=True):
    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id")
    user_id: int = Field(foreign_key="users.id")
    status: NotificationStatus = Field(default=NotificationStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)