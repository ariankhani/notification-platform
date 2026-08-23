from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel


class AttemptStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class DeliveryAttemptBase(SQLModel):
    attempt_number: int
    status: AttemptStatus
    error_message: str | None = None


class DeliveryAttemptResponse(DeliveryAttemptBase):
    id: int
    notification_id: int
    attempted_at: datetime