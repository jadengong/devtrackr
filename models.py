import enum
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Text, DateTime, Enum, Boolean, Index, func )
from sqlalchemy.orm import Mapped, mapped_column
from db import Base # adjust import if db.py is in a package

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),      # Postgres ENUM type named "task_status"
        nullable=False,
        default=TaskStatus.todo,                   # client-side default
        server_default=TaskStatus.todo.value,      # DB-side default
        index=True,
    )

    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3, server_default="3")  # 1–5 
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false", index=True)

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
<<<<<<< Updated upstream
=======
        Index("ix_tasks_owner_status", "owner_id", "status"),
        Index("ix_tasks_category", "category"),
>>>>>>> Stashed changes
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} status={self.status} prio={self.priority}>"