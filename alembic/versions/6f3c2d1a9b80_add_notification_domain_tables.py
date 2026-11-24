"""add notification domain tables

Revision ID: 6f3c2d1a9b80
Revises: bf42b59dd962
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "6f3c2d1a9b80"
down_revision: str | Sequence[str] | None = "bf42b59dd962"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

event_status = sa.Enum(
    "RECEIVED", "PROCESSING", "PROCESSED", "FAILED", name="eventstatus"
)
notification_status = sa.Enum(
    "PENDING",
    "QUEUED",
    "SENDING",
    "SENT",
    "FAILED",
    "CANCELLED",
    name="notificationstatus",
)
attempt_status = sa.Enum("SUCCESS", "FAILED", name="attemptstatus")


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("platform", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("status", event_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_events_event_type", "events", ["event_type"])

    op.create_table(
        "roles",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    op.create_table(
        "notification_rules",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.UniqueConstraint(
            "event_type",
            "role_id",
            "channel",
            name="uq_notification_rule_event_role_channel",
        ),
    )
    op.create_index(
        "ix_notification_rules_event_type", "notification_rules", ["event_type"]
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("role_id", sa.Integer(), primary_key=True, nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("rule_id", sa.Integer(), nullable=True),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("message", sa.String(length=5000), nullable=False),
        sa.Column("status", notification_status, nullable=False),
        sa.Column("rendered_content", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["rule_id"], ["notification_rules.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("ix_notifications_event_id", "notifications", ["event_id"])
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])

    op.create_table(
        "delivery_attempts",
        sa.Column("notification_id", sa.Integer(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("status", attempt_status, nullable=False),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("attempted_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["notification_id"], ["notifications.id"]),
    )


def downgrade() -> None:
    op.drop_table("delivery_attempts")
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_index("ix_notifications_event_id", table_name="notifications")
    op.drop_table("notifications")
    op.drop_table("user_roles")
    op.drop_index(
        "ix_notification_rules_event_type", table_name="notification_rules"
    )
    op.drop_table("notification_rules")
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
    op.drop_index("ix_events_event_type", table_name="events")
    op.drop_table("events")
    attempt_status.drop(op.get_bind(), checkfirst=True)
    notification_status.drop(op.get_bind(), checkfirst=True)
    event_status.drop(op.get_bind(), checkfirst=True)
