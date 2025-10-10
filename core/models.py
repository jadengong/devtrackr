import enum
from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    Boolean,
    Index,
    func,
    ForeignKey,
    JSON,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base  # adjust import if db.py is in a package


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


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship to tasks
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )

    # Relationship to time entries
    time_entries: Mapped[list["TimeEntry"]] = relationship(
        "TimeEntry", back_populates="owner", cascade="all, delete-orphan"
    )

    # Relationship to activity logs
    activity_logs: Mapped[list["ActivityLog"]] = relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} email={self.email!r}>"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),  # Postgres ENUM type named "task_status"
        nullable=False,
        default=TaskStatus.todo,  # client-side default
        server_default=TaskStatus.todo.value,  # DB-side default
        index=True,
    )

    priority: Mapped[TaskPriority] = mapped_column(
        Enum(
            TaskPriority, name="task_priority"
        ),  # Postgres ENUM type named "task_priority"
        nullable=False,
        default=TaskPriority.medium,  # client-side default
        server_default=TaskPriority.medium.value,  # DB-side default
        index=True,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    estimated_minutes: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Estimated time to complete
    actual_minutes: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Actual time spent

    is_archived: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True
    )

    # User relationship
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    owner: Mapped[User] = relationship("User", back_populates="tasks")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # set by DB at insert
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # set by DB at insert
        onupdate=func.now(),  # set by ORM on UPDATE
    )

    __table_args__ = (
        Index("ix_tasks_status_due", "status", "due_date"),
        Index("ix_tasks_owner_status", "owner_id", "status"),
        # Removed duplicate priority index since priority column has index=True
        Index("ix_tasks_owner_priority", "owner_id", "priority"),
    )

    def __repr__(self) -> str:
        return (
            f"<Task id={self.id} title={self.title!r} "
            f"status={self.status} priority={self.priority}>"
        )


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=False, index=True
    )
    task: Mapped[Task] = relationship("Task")

    # Time tracking fields
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[TimeEntryStatus] = mapped_column(
        Enum(TimeEntryStatus, name="time_entry_status"),
        nullable=False,
        default=TimeEntryStatus.active,
        server_default=TimeEntryStatus.active.value,
        index=True,
    )

    # Additional tracking
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # User relationship (through task)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    owner: Mapped[User] = relationship("User")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        Index("ix_time_entries_owner_status", "owner_id", "status"),
        Index("ix_time_entries_task_start", "task_id", "start_time"),
        Index("ix_time_entries_owner_date", "owner_id", "start_time"),
    )

    def __repr__(self) -> str:
        return (
            f"<TimeEntry id={self.id} task_id={self.task_id} "
            f"status={self.status} duration={self.duration_minutes}>"
        )


class ActivityType(str, enum.Enum):
    """Activity types for the activity log."""

    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ARCHIVED = "task_archived"
    TASK_UNARCHIVED = "task_unarchived"
    TIMER_STARTED = "timer_started"
    TIMER_STOPPED = "timer_stopped"


class ActivityLog(Base):
    """Activity log for tracking recent user actions."""

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type = Column(Enum(ActivityType), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # "task", "time_entry", etc.
    entity_id = Column(Integer, nullable=True)  # ID of the affected entity
    description = Column(Text, nullable=False)  # Human-readable description
    activity_metadata = Column(
        JSON, nullable=True
    )  # Additional data (old values, etc.)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationship
    user = relationship("User", back_populates="activity_logs")

    __table_args__ = (
        Index("ix_activity_logs_user_created", "user_id", "created_at"),
        Index("ix_activity_logs_type_created", "activity_type", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<ActivityLog id={self.id} user_id={self.user_id} "
            f"type={self.activity_type} entity={self.entity_type}:{self.entity_id}>"
        )
