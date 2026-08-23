from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class NotificationStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"



class NotificationRuleBase(SQLModel):
    event_type: str = Field(index=True)
    channel: str
    is_active: bool = Field(default=True)


class NotificationRuleCreate(NotificationRuleBase):
    role_id: int


class NotificationRuleResponse(NotificationRuleBase):
    id: int
    role_id: int



class NotificationBase(SQLModel):
    channel: str
    message: str


class NotificationResponse(NotificationBase):
    id: int
    event_id: int
    user_id: int
    status: NotificationStatus
    created_at: datetime
