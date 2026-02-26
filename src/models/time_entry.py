"""TimeEntry model definition."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base
from .base import TimeEntryStatus

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=False, index=True
    )
    task: Mapped[Task] = relationship("Task")

    # Time tracking fields
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[TimeEntryStatus] = mapped_column(
        Enum(TimeEntryStatus, name="time_entry_status"),
        nullable=False,
        default=TimeEntryStatus.active,
        server_default=TimeEntryStatus.active.value,
        index=True,
    )

    # Additional tracking
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # User relationship (through task)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    owner: Mapped[User] = relationship("User")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        Index("ix_time_entries_owner_status", "owner_id", "status"),
        Index("ix_time_entries_task_start", "task_id", "start_time"),
        Index("ix_time_entries_owner_date", "owner_id", "start_time"),
    )

    def __repr__(self) -> str:
        return (
            f"<TimeEntry id={self.id} task_id={self.task_id} "
            f"status={self.status} duration={self.duration_minutes}>"
        )
