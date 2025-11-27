from typing import List, Optional
from datetime import datetime
import time
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func, text
from core.models import Task, TaskStatus, TaskPriority, User
from core.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskListResponse,
    TaskSearchResponse,
    SearchFilters,
)
from core.deps import get_db, get_current_active_user
from utils.pagination import create_task_cursor, get_pagination_params
from utils.search_utils import (
    build_search_query,
    get_search_suggestions,
    normalize_search_query,
    calculate_search_stats,
)
from services.activity_logger import ActivityLogger

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

    # Log activity
    ActivityLogger.log_task_created(
        db=db,
        user_id=current_user.id,
        task_id=task.id,
        task_title=task.title,
    )

    return task


@router.get("", response_model=TaskListResponse)
def list_tasks(
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of tasks per page"),
    status_: Optional[TaskStatus] = Query(None, alias="status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    due_before: Optional[datetime] = None,
    archived: Optional[bool] = None,
    include_total: bool = Query(
        False, description="Include total count (expensive for large datasets)"
    ),
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
        stmt = stmt.where(Task.due_date.isnot(None), Task.due_date <= due_before)
    if archived is not None:
        stmt = stmt.where(Task.is_archived == archived)

    # Apply cursor-based pagination
    if cursor_id and cursor_created_at:
        # For cursor pagination, we need to handle the case where multiple tasks
        # have the same created_at timestamp by using ID as a tiebreaker
        stmt = stmt.where(
            or_(
                Task.created_at < cursor_created_at,
                and_(Task.created_at == cursor_created_at, Task.id < cursor_id),
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
        items=tasks, next_cursor=next_cursor, has_next=has_next, total_count=total_count
    )


@router.get("/search", response_model=TaskSearchResponse)
def search_tasks(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    status_: Optional[TaskStatus] = Query(
        None, alias="status", description="Filter by status"
    ),
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    created_after: Optional[datetime] = Query(
        None, description="Filter tasks created after this date"
    ),
    created_before: Optional[datetime] = Query(
        None, description="Filter tasks created before this date"
    ),
    due_after: Optional[datetime] = Query(
        None, description="Filter tasks due after this date"
    ),
    due_before: Optional[datetime] = Query(
        None, description="Filter tasks due before this date"
    ),
    archived: Optional[bool] = Query(None, description="Filter by archived status"),
    include_suggestions: bool = Query(True, description="Include search suggestions"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search tasks using full-text search across titles and descriptions."""

    start_time = time.time()

    # Normalize search query
    normalized_query = normalize_search_query(q)
    if not normalized_query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty or contain only special characters",
        )

    # Build search filters
    filters = SearchFilters(
        status=status_,
        category=category,
        priority=priority,
        created_after=created_after,
        created_before=created_before,
        due_after=due_after,
        due_before=due_before,
        archived=archived,
    )

    # Build the search query
    search_sql, params = build_search_query(normalized_query, filters, current_user.id)

    # Add limit to the query
    search_sql += (
        f" LIMIT {limit + 1}"  # Get one extra to check if there are more results
    )

    # Execute search query
    try:
        result = db.execute(text(search_sql), params)
        tasks = result.fetchall()

        # Check if there are more results
        has_more = len(tasks) > limit
        if has_more:
            tasks = tasks[:limit]  # Remove the extra item

        # Convert to Task objects
        task_objects = []
        for row in tasks:
            # Create Task object from row data
            task = Task(
                id=row.id,
                title=row.title,
                description=row.description,
                category=row.category,
                status=TaskStatus(row.status),
                priority=TaskPriority(row.priority),
                due_date=row.due_date,
                estimated_minutes=row.estimated_minutes,
                actual_minutes=row.actual_minutes,
                is_archived=row.is_archived,
                owner_id=row.owner_id,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            task_objects.append(task)

        # Get total count for the search (without limit)
        count_sql = (
            search_sql.replace(
                "SELECT t.*, ts_rank(to_tsvector('english', t.title || ' ' || COALESCE(t.description, '')), plainto_tsquery('english', :query)) as rank",
                "SELECT COUNT(*) as total",
            ).split("ORDER BY")[0]
            + "LIMIT 1"
        )

        count_result = db.execute(text(count_sql), params)
        total_matches = count_result.scalar() or 0

        # Get search suggestions if requested
        suggestions = None
        if include_suggestions:
            suggestions = get_search_suggestions(db, current_user.id, normalized_query)

        # Calculate search statistics
        search_stats = calculate_search_stats(
            start_time, total_matches, normalized_query
        )

        return TaskSearchResponse(
            items=task_objects,
            query=normalized_query,
            total_matches=total_matches,
            search_time_ms=search_stats["search_time_ms"],
            suggestions=suggestions,
        )

    except Exception as e:
        # Log the error and return a user-friendly message
        raise HTTPException(
            status_code=500,
            detail="Search failed. Please try a different query or contact support.",
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


@router.post("/{task_id}/unarchive", response_model=TaskOut)
def unarchive_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Unarchive a task (must belong to current user)."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this task"
        )

    if not task.is_archived:
        raise HTTPException(status_code=400, detail="Task is not archived")

    task.is_archived = False
    db.add(task)
    db.commit()
    db.refresh(task)

    # Log activity
    ActivityLogger.log_task_unarchived(
        db=db,
        user_id=current_user.id,
        task_id=task.id,
        task_title=task.title,
    )

    return task


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
