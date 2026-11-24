"""Import every table model so SQLModel metadata is always complete."""

from app.models.delivery import DeliveryAttempt
from app.models.event import Event
from app.models.role import Role, UserRole
from app.models.user import User
from app.modules.notifications.models import Notification, NotificationRule

__all__ = [
    "DeliveryAttempt",
    "Event",
    "Notification",
    "NotificationRule",
    "Role",
    "User",
    "UserRole",
]
