"""Task-related schemas."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from ..models.base import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = Field(None, ge=1)  # Minimum 1 minute
    actual_minutes: Optional[int] = Field(None, ge=0)  # Minimum 0 minutes


class TaskCreate(TaskBase):
    title: str


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = Field(None, ge=1)
    actual_minutes: Optional[int] = Field(None, ge=0)
    is_archived: Optional[bool] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Paginated task list response"""

    items: List[TaskOut]
    next_cursor: Optional[str] = None
    has_next: bool = False
    total_count: Optional[int] = None


class TaskSearchResponse(BaseModel):
    """Search results response"""

    items: List[TaskOut]
    query: str
    total_matches: int
    search_time_ms: float
    suggestions: Optional[List[str]] = None


class SearchFilters(BaseModel):
    """Search filters."""

    model_config = ConfigDict(str_strip_whitespace=True)

    status: Optional[TaskStatus] = None
    category: Optional[str] = None
    priority: Optional[TaskPriority] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    due_before: Optional[datetime] = None
    archived: Optional[bool] = None
