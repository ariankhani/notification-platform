from datetime import datetime

from sqlmodel import Field

from app.schemas.event import EventBase, EventStatus


class Event(EventBase, table=True):
    __tablename__ = "events"

    id: int | None = Field(default=None, primary_key=True)
    status: EventStatus = Field(default=EventStatus.RECEIVED)
    created_at: datetime = Field(default_factory=datetime.utcnow)