"""
Base model configuration and enums.

Provides the SQLAlchemy Base class and shared enumerations.
"""

from enum import StrEnum

from ..core.database import Base


class TaskStatus(StrEnum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TimeEntryStatus(StrEnum):
    active = "active"
    paused = "paused"
    completed = "completed"


class ActivityType(StrEnum):
    """Activity types for the activity log."""

    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ARCHIVED = "task_archived"
    TASK_UNARCHIVED = "task_unarchived"
    TIMER_STARTED = "timer_started"
    TIMER_STOPPED = "timer_stopped"


__all__ = [
    "Base",
    "TaskStatus",
    "TaskPriority",
    "TimeEntryStatus",
    "ActivityType",
]
