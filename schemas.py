from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from models import TaskStatus, TaskPriority


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Task Schemas
class TaskBase(BaseModel):
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
    id: int
    owner_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Metrics Schemas
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
