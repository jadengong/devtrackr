"""Time entry and timer schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..models.base import TimeEntryStatus


class TimeEntryBase(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)


class TimeEntryCreate(TimeEntryBase):
    task_id: int


class TimeEntryUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    end_time: Optional[datetime] = None


class TimeEntryOut(TimeEntryBase):
    id: int
    task_id: int
    owner_id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    status: TimeEntryStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimerStart(BaseModel):
    task_id: int
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)


class TimerStop(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)


class ActiveTimer(BaseModel):
    time_entry_id: int
    task_id: int
    task_title: str
    start_time: datetime
    elapsed_minutes: int
    description: Optional[str]
    category: Optional[str]


class TimeSummary(BaseModel):
    total_time_minutes: int
    total_entries: int
    average_session_minutes: float
    most_productive_category: Optional[str]
    today_time_minutes: int
    this_week_time_minutes: int
