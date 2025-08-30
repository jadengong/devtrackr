from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models import TaskStatus 

class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(default=3, ge=1, le=5)
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_date: Optional[datetime] = None
    is_archived: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # pydantic v2: accepts ORM objects directly
