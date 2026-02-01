"""Metrics-related schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskMetrics(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    todo_tasks: int
    total_estimated_minutes: Optional[int]
    total_actual_minutes: Optional[int]
    completion_rate: float  # Percentage of completed tasks


class CategoryBreakdown(BaseModel):
    category: str
    count: int
    estimated_minutes: Optional[int]
    actual_minutes: Optional[int]


class WeeklyStats(BaseModel):
    week_start: datetime
    week_end: datetime
    tasks_completed: int
    total_time_spent: Optional[int]  # in minutes
    productivity_score: float  # based on completion rate and time efficiency
