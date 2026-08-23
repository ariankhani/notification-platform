from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class EventStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class EventBase(SQLModel):
    platform: str
    event_type: str = Field(index=True)
    message: str


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    status: EventStatus
    created_at: datetime