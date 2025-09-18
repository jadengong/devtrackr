from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from models import Task, TaskStatus, TaskPriority, User
from schemas import TaskCreate, TaskUpdate, TaskOut, TaskListResponse
from deps import get_db, get_current_active_user
from pagination import create_task_cursor, get_pagination_params

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
        priority=payload.priority or TaskPriority.medium,
        due_date=payload.due_date,
        estimated_minutes=payload.estimated_minutes,
        actual_minutes=payload.actual_minutes,
        owner_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=TaskListResponse)
def list_tasks(
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of tasks per page"),
    status_: Optional[TaskStatus] = Query(None, alias="status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    due_before: Optional[datetime] = None,
    archived: Optional[bool] = None,
    include_total: bool = Query(False, description="Include total count (expensive for large datasets)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List tasks for the current user with cursor-based pagination and optional filters."""
    
    # Parse pagination parameters
    cursor_id, cursor_created_at, limit = get_pagination_params(cursor, limit)
    
    # Build base query
    stmt = select(Task).where(Task.owner_id == current_user.id)
    
    # Apply filters
    if status_ is not None:
        stmt = stmt.where(Task.status == status_)
    if category is not None:
        stmt = stmt.where(Task.category == category)
    if due_before is not None:
        stmt = stmt.where(
            Task.due_date.isnot(None), Task.due_date <= due_before
        )
    if archived is not None:
        stmt = stmt.where(Task.is_archived == archived)
    
    # Apply cursor-based pagination
    if cursor_id and cursor_created_at:
        # For cursor pagination, we need to handle the case where multiple tasks
        # have the same created_at timestamp by using ID as a tiebreaker
        stmt = stmt.where(
            or_(
                Task.created_at < cursor_created_at,
                and_(
                    Task.created_at == cursor_created_at,
                    Task.id < cursor_id
                )
            )
        )
    
    # Order by created_at desc, then by id desc for consistent pagination
    stmt = stmt.order_by(Task.created_at.desc(), Task.id.desc())
    
    # Get one extra item to determine if there's a next page
    stmt = stmt.limit(limit + 1)
    
    # Execute query
    tasks = db.execute(stmt).scalars().all()
    
    # Check if there are more items
    has_next = len(tasks) > limit
    if has_next:
        tasks = tasks[:limit]  # Remove the extra item
    
    # Create next cursor if there are more items
    next_cursor = None
    if has_next and tasks:
        last_task = tasks[-1]
        next_cursor = create_task_cursor(last_task.id, last_task.created_at)
    
    # Get total count if requested (expensive for large datasets)
    total_count = None
    if include_total:
        count_stmt = select(func.count(Task.id)).where(Task.owner_id == current_user.id)
        
        # Apply the same filters as the main query
        if status_ is not None:
            count_stmt = count_stmt.where(Task.status == status_)
        if category is not None:
            count_stmt = count_stmt.where(Task.category == category)
        if due_before is not None:
            count_stmt = count_stmt.where(
                Task.due_date.isnot(None), Task.due_date <= due_before
            )
        if archived is not None:
            count_stmt = count_stmt.where(Task.is_archived == archived)
        
        total_count = db.execute(count_stmt).scalar()
    
    return TaskListResponse(
        items=tasks,
        next_cursor=next_cursor,
        has_next=has_next,
        total_count=total_count
    )


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
    if "priority" in updates and updates["priority"] is not None:
        updates["priority"] = TaskPriority(updates["priority"])

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
    """Start timing a task (redirects to new time tracking system)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this task"
        )

    # Redirect to new time tracking system
    from routers.time_tracking import start_timer
    from schemas import TimerStart

    timer_data = TimerStart(task_id=task_id)
    return start_timer(timer_data, db, current_user)


@router.post("/{task_id}/stop-timer")
def stop_task_timer(
    task_id: int,
    minutes_spent: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Stop timing a task and record time spent (legacy endpoint)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this task"
        )

    # Update actual time spent (legacy behavior)
    if task.actual_minutes is None:
        task.actual_minutes = minutes_spent
    else:
        task.actual_minutes += minutes_spent

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Timer stopped (legacy endpoint - consider using /time/stop/{time_entry_id})",
        "task_id": task_id,
        "total_minutes": task.actual_minutes,
    }
