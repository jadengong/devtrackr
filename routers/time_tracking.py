from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from core.models import Task, TimeEntry, TimeEntryStatus, User
from core.schemas import (
    TimeEntryUpdate,
    TimeEntryOut,
    TimerStart,
    TimerStop,
    ActiveTimer,
    TimeSummary,
)
from core.deps import get_db, get_current_active_user

router = APIRouter(prefix="/time", tags=["time-tracking"])


@router.post("/start", response_model=TimeEntryOut, status_code=status.HTTP_201_CREATED)
def start_timer(
    timer_data: TimerStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Start a timer for a specific task."""
    # Check if task exists and belongs to user
    task = db.get(Task, timer_data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to track time for this task"
        )

    # Check if there's already an active timer for this user
    active_timer = db.execute(
        select(TimeEntry).where(
            and_(
                TimeEntry.owner_id == current_user.id,
                TimeEntry.status == TimeEntryStatus.active,
            )
        )
    ).scalar_one_or_none()

    if active_timer:
        raise HTTPException(
            status_code=400,
            detail=f"You already have an active timer for task '{active_timer.task.title}'",
        )

    # Create new time entry
    time_entry = TimeEntry(
        task_id=timer_data.task_id,
        owner_id=current_user.id,
        start_time=datetime.now(timezone.utc),
        description=timer_data.description,
        category=timer_data.category,
        status=TimeEntryStatus.active,
    )

    db.add(time_entry)
    db.commit()
    db.refresh(time_entry)
    return time_entry


@router.post("/stop/{time_entry_id}", response_model=TimeEntryOut)
def stop_timer(
    time_entry_id: int,
    timer_data: Optional[TimerStop] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Stop an active timer."""
    time_entry = db.get(TimeEntry, time_entry_id)
    if not time_entry:
        raise HTTPException(status_code=404, detail="Time entry not found")

    if time_entry.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this time entry"
        )

    if time_entry.status != TimeEntryStatus.active:
        raise HTTPException(status_code=400, detail="Timer is not active")

    # Calculate duration
    end_time = datetime.now(timezone.utc)
    # Ensure start_time is timezone-aware for comparison
    start_time = time_entry.start_time
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    duration_minutes = int((end_time - start_time).total_seconds() / 60)

    # Update time entry
    time_entry.end_time = end_time
    time_entry.duration_minutes = duration_minutes
    time_entry.status = TimeEntryStatus.completed

    if timer_data:
        if timer_data.description:
            time_entry.description = timer_data.description
        if timer_data.category:
            time_entry.category = timer_data.category

    # Update task's actual time
    if time_entry.task.actual_minutes is None:
        time_entry.task.actual_minutes = duration_minutes
    else:
        time_entry.task.actual_minutes += duration_minutes

    db.add(time_entry)
    db.add(time_entry.task)
    db.commit()
    db.refresh(time_entry)
    return time_entry


@router.get("/active", response_model=Optional[ActiveTimer])
def get_active_timer(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get the currently active timer for the user."""
    active_timer = db.execute(
        select(TimeEntry).where(
            and_(
                TimeEntry.owner_id == current_user.id,
                TimeEntry.status == TimeEntryStatus.active,
            )
        )
    ).scalar_one_or_none()

    if not active_timer:
        return None

    # Calculate elapsed time
    current_time = datetime.now(timezone.utc)
    start_time = active_timer.start_time
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    elapsed_minutes = int((current_time - start_time).total_seconds() / 60)

    return ActiveTimer(
        time_entry_id=active_timer.id,
        task_id=active_timer.task_id,
        task_title=active_timer.task.title,
        start_time=active_timer.start_time,
        elapsed_minutes=elapsed_minutes,
        description=active_timer.description,
        category=active_timer.category,
    )


@router.get("/entries", response_model=List[TimeEntryOut])
def list_time_entries(
    task_id: Optional[int] = Query(None, description="Filter by task ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(50, ge=1, le=100, description="Number of entries to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List time entries with optional filters."""
    stmt = select(TimeEntry).where(TimeEntry.owner_id == current_user.id)

    if task_id is not None:
        stmt = stmt.where(TimeEntry.task_id == task_id)
    if category is not None:
        stmt = stmt.where(TimeEntry.category == category)
    if date_from is not None:
        stmt = stmt.where(TimeEntry.start_time >= date_from)
    if date_to is not None:
        stmt = stmt.where(TimeEntry.start_time <= date_to)

    time_entries = (
        db.execute(stmt.order_by(TimeEntry.start_time.desc()).limit(limit))
        .scalars()
        .all()
    )

    return time_entries


@router.get("/summary", response_model=TimeSummary)
def get_time_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get time tracking summary for the specified period."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    # Get total time and entries in period
    total_stats = db.execute(
        select(
            func.sum(TimeEntry.duration_minutes).label("total_time"),
            func.count(TimeEntry.id).label("total_entries"),
            func.avg(TimeEntry.duration_minutes).label("avg_duration"),
        ).where(
            and_(
                TimeEntry.owner_id == current_user.id,
                TimeEntry.status == TimeEntryStatus.completed,
                TimeEntry.start_time >= start_date,
                TimeEntry.start_time <= end_date,
            )
        )
    ).first()

    # Get most productive category
    category_stats = db.execute(
        select(
            TimeEntry.category,
            func.sum(TimeEntry.duration_minutes).label("category_time"),
        )
        .where(
            and_(
                TimeEntry.owner_id == current_user.id,
                TimeEntry.status == TimeEntryStatus.completed,
                TimeEntry.start_time >= start_date,
                TimeEntry.start_time <= end_date,
                TimeEntry.category.isnot(None),
            )
        )
        .group_by(TimeEntry.category)
        .order_by(func.sum(TimeEntry.duration_minutes).desc())
        .limit(1)
    ).first()

    # Get today's time
    today_start = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    today_time = (
        db.execute(
            select(func.sum(TimeEntry.duration_minutes)).where(
                and_(
                    TimeEntry.owner_id == current_user.id,
                    TimeEntry.status == TimeEntryStatus.completed,
                    TimeEntry.start_time >= today_start,
                )
            )
        ).scalar()
        or 0
    )

    # Get this week's time
    week_start = end_date - timedelta(days=end_date.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_time = (
        db.execute(
            select(func.sum(TimeEntry.duration_minutes)).where(
                and_(
                    TimeEntry.owner_id == current_user.id,
                    TimeEntry.status == TimeEntryStatus.completed,
                    TimeEntry.start_time >= week_start,
                )
            )
        ).scalar()
        or 0
    )

    return TimeSummary(
        total_time_minutes=total_stats.total_time or 0,
        total_entries=total_stats.total_entries or 0,
        average_session_minutes=round(total_stats.avg_duration or 0, 2),
        most_productive_category=category_stats.category if category_stats else None,
        today_time_minutes=today_time,
        this_week_time_minutes=week_time,
    )


@router.patch("/entries/{time_entry_id}", response_model=TimeEntryOut)
def update_time_entry(
    time_entry_id: int,
    update_data: TimeEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a time entry."""
    time_entry = db.get(TimeEntry, time_entry_id)
    if not time_entry:
        raise HTTPException(status_code=404, detail="Time entry not found")

    if time_entry.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this time entry"
        )

    # Update fields
    updates = update_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(time_entry, field, value)

    # Recalculate duration if end_time was updated
    if "end_time" in updates and updates["end_time"] and time_entry.start_time:
        end_time = time_entry.end_time
        start_time = time_entry.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        time_entry.duration_minutes = duration_minutes

    db.add(time_entry)
    db.commit()
    db.refresh(time_entry)
    return time_entry


@router.delete("/entries/{time_entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_entry(
    time_entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a time entry."""
    time_entry = db.get(TimeEntry, time_entry_id)
    if not time_entry:
        raise HTTPException(status_code=404, detail="Time entry not found")

    if time_entry.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this time entry"
        )

    # Subtract time from task's actual_minutes if it was completed
    if (
        time_entry.status == TimeEntryStatus.completed
        and time_entry.duration_minutes
        and time_entry.task.actual_minutes
    ):
        time_entry.task.actual_minutes = max(
            0, time_entry.task.actual_minutes - time_entry.duration_minutes
        )
        db.add(time_entry.task)

    db.delete(time_entry)
    db.commit()
    return None
