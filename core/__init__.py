"""
Core application components for DevTrackr.

This package contains the fundamental building blocks of the application:
- models: SQLAlchemy ORM models
- schemas: Pydantic models for request/response validation
- db: Database connection and session management
- deps: Dependency injection functions
"""

from .models import *
from .schemas import *
from .db import *
from .deps import *

__all__ = [
    # Models exports
    "User",
    "Task", 
    "TimeEntry",
    "ActivityLog",
    "TaskStatus",
    "TaskPriority",
    "TimeEntryStatus",
    "ActivityType",
    
    # Schemas exports
    "UserCreate",
    "UserLogin", 
    "UserOut",
    "Token",
    "TaskCreate",
    "TaskUpdate",
    "TaskOut",
    "TaskListResponse",
    "TaskSearchResponse",
    "SearchFilters",
    "TimeEntryCreate",
    "TimeEntryUpdate", 
    "TimeEntryOut",
    "TimeEntryListResponse",
    "ActivityLogOut",
    "ActivityLogListResponse",
    "TaskMetrics",
    "CategoryBreakdown",
    "WeeklyStats",
    
    # Database exports
    "engine",
    "SessionLocal",
    "get_db",
    "Base",
    
    # Dependencies exports
    "get_password_hash",
    "verify_password",
    "create_access_token",
    "get_current_user",
    "get_current_active_user",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
]
