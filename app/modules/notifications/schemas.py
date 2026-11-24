from datetime import datetime

from pydantic import BaseModel, Field

from .models import NotificationStatus


class NotificationRuleBase(BaseModel):
    event_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    channel: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    is_active: bool = True


class NotificationRuleCreate(NotificationRuleBase):
    role_id: int = Field(
        ...,
        gt=0,
    )


class NotificationRuleUpdate(BaseModel):
    event_type: str | None = Field(None, min_length=1, max_length=100)
    channel: str | None = Field(None, min_length=1, max_length=50)
    role_id: int | None = Field(None, gt=0)
    is_active: bool | None = None


class NotificationRuleResponse(NotificationRuleBase):
    id: int
    role_id: int
    created_at: datetime
    updated_at: datetime | None = None


class NotificationBase(BaseModel):
    channel: str = Field(..., max_length=50)
    message: str = Field(..., min_length=1, max_length=5000)


class NotificationCreate(NotificationBase):
    event_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    rule_id: int | None = Field(None, gt=0)


class NotificationResponse(NotificationBase):
    id: int
    event_id: int
    user_id: int
    rule_id: int | None = None
    status: NotificationStatus
    rendered_content: dict | None = None
    error_message: str | None = None
    created_at: datetime
    sent_at: datetime | None = None
