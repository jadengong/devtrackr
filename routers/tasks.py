from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Task, TaskStatus, User
from schemas import TaskCreate, TaskUpdate, TaskOut
from deps import get_db, get_current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new task for the current user."""
    task = Task(
        title=payload.title,
        description=payload.description,
        category=payload.category,
        status=TaskStatus(payload.status) if payload.status else TaskStatus.todo,
        priority=payload.priority or 3,
        due_date=payload.due_date,
        estimated_minutes=payload.estimated_minutes,
        actual_minutes=payload.actual_minutes,
        owner_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=List[TaskOut])
def list_tasks(
    status_: Optional[TaskStatus] = Query(None, alias="status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    due_before: Optional[datetime] = None,
    archived: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List tasks for the current user with optional filters."""
    stmt = select(Task).where(Task.owner_id == current_user.id)

    if status_ is not None:
        stmt = stmt.where(Task.status == status_)
    if category is not None:
        stmt = stmt.where(Task.category == category)
    if due_before is not None:
        stmt = stmt.where(
            Task.due_date.isnot(None), Task.due_date <= due_before
        )  # noqa: E711
    if archived is not None:
        stmt = stmt.where(Task.is_archived == archived)

    tasks = db.execute(stmt.order_by(Task.created_at.desc())).scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific task by ID (must belong to current user)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this task"
        )

    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a task (must belong to current user)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this task"
        )

    updates = payload.model_dump(exclude_unset=True)
    if "status" in updates and updates["status"] is not None:
        updates["status"] = TaskStatus(updates["status"])

    for field, value in updates.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    hard: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a task (soft delete by default, must belong to current user)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this task"
        )

    if hard:
        db.delete(task)
    else:
        task.is_archived = True
        db.add(task)
    db.commit()
    return None


@router.post("/{task_id}/start-timer")
def start_task_timer(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Start timing a task (placeholder for future timer functionality)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this task"
        )

    # TODO: Implement actual timer functionality
    return {"message": "Timer started for task", "task_id": task_id}


@router.post("/{task_id}/stop-timer")
def stop_task_timer(
    task_id: int,
    minutes_spent: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Stop timing a task and record time spent."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this task"
        )

    # Update actual time spent
    if task.actual_minutes is None:
        task.actual_minutes = minutes_spent
    else:
        task.actual_minutes += minutes_spent

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Timer stopped",
        "task_id": task_id,
        "total_minutes": task.actual_minutes,
    }
