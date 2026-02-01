"""
Schemas package.

Re-exports all Pydantic schemas for convenient importing.
"""

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserOut,
    UserLogin,
    Token,
    TokenData,
)
from .task import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskListResponse,
    TaskSearchResponse,
    SearchFilters,
)
from .time_entry import (
    TimeEntryBase,
    TimeEntryCreate,
    TimeEntryUpdate,
    TimeEntryOut,
    TimerStart,
    TimerStop,
    ActiveTimer,
    TimeSummary,
)
from .metrics import (
    TaskMetrics,
    CategoryBreakdown,
    WeeklyStats,
)
from .activity import (
    ActivityLogOut,
    ActivityLogListResponse,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "UserLogin",
    "Token",
    "TokenData",
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskOut",
    "TaskListResponse",
    "TaskSearchResponse",
    "SearchFilters",
    # Time entry schemas
    "TimeEntryBase",
    "TimeEntryCreate",
    "TimeEntryUpdate",
    "TimeEntryOut",
    "TimerStart",
    "TimerStop",
    "ActiveTimer",
    "TimeSummary",
    # Metrics schemas
    "TaskMetrics",
    "CategoryBreakdown",
    "WeeklyStats",
    # Activity schemas
    "ActivityLogOut",
    "ActivityLogListResponse",
]
