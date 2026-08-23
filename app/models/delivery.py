from datetime import datetime

from sqlmodel import Field

from app.schemas.delivery import DeliveryAttemptBase


class DeliveryAttempt(DeliveryAttemptBase, table=True):
    __tablename__ = "delivery_attempts"

    id: int | None = Field(default=None, primary_key=True)
    notification_id: int = Field(foreign_key="notifications.id")
    attempted_at: datetime = Field(default_factory=datetime.utcnow)