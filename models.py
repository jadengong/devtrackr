import enum
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Text, DateTime, Enum, Boolean, Index, func, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base # adjust import if db.py is in a package

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship to tasks
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} email={self.email!r}>"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),      # Postgres ENUM type named "task_status"
        nullable=False,
        default=TaskStatus.todo,                   # client-side default
        server_default=TaskStatus.todo.value,      # DB-side default
        index=True,
    )

    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3, server_default="3")  # 1–5 
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Estimated time to complete
    actual_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)     # Actual time spent

    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false", index=True)

    # User relationship
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner: Mapped[User] = relationship("User", back_populates="tasks")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),                 # set by DB at insert
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),                 # set by DB at insert
        onupdate=func.now(),                       # set by ORM on UPDATE
    )

    __table_args__ = (
        Index("ix_tasks_status_due", "status", "due_date"),
        Index("ix_tasks_owner_status", "owner_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} status={self.status} prio={self.priority}>"