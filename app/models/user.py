from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from app.modules.notifications.models import Notification

from app.schemas.user import UserBase


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    hashed_refresh_token: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    notifications: list["Notification"] = Relationship(back_populates="user")
