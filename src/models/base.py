"""
Base model configuration and enums.

Provides the SQLAlchemy Base class and shared enumerations.
"""

import enum
from ..core.database import Base


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TimeEntryStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    completed = "completed"


class ActivityType(str, enum.Enum):
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
