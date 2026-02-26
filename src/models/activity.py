"""ActivityLog model definition."""

from __future__ import annotations

from datetime import datetime, timezone as tz
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    Index,
    ForeignKey,
    JSON,
    Column,
)
from sqlalchemy.orm import relationship

from ..core.database import Base
from .base import ActivityType

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class ActivityLog(Base):
    """Activity log for tracking recent user actions."""

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type = Column(Enum(ActivityType), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # "task", "time_entry", etc.
    entity_id = Column(Integer, nullable=True)  # ID of the affected entity
    description = Column(Text, nullable=False)  # Human-readable description
    activity_metadata = Column(
        JSON, nullable=True
    )  # Additional data (old values, etc.)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz.utc),
        nullable=False,
        index=True,
    )

    # Relationship
    user = relationship("User", back_populates="activity_logs")

    __table_args__ = (
        Index("ix_activity_logs_user_created", "user_id", "created_at"),
        Index("ix_activity_logs_type_created", "activity_type", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<ActivityLog id={self.id} user_id={self.user_id} "
            f"type={self.activity_type} entity={self.entity_type}:{self.entity_id}>"
        )
