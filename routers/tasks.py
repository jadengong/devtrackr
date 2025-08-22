from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Task, TaskStatus
from schemas import TaskCreate, TaskUpdate, TaskOut
from deps import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=payload.title,
        description=payload.description,
        status=TaskStatus(payload.status) if payload.status else TaskStatus.todo,
        priority=payload.priority or 3,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()       # writes and ends transaction
    db.refresh(task)  # re-loads auto fields (id, timestamps)
    return task

@router.get("", response_model=List[TaskOut])
def list_tasks(
    status_: Optional[TaskStatus] = Query(None, alias="status"),
    due_before: Optional[datetime] = None,
    archived: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    stmt = select(Task)
    if status_ is not None:
        stmt = stmt.where(Task.status == status_)
    if due_before is not None:
        stmt = stmt.where(Task.due_date != None, Task.due_date <= due_before)  # noqa: E711
    if archived is not None:
        stmt = stmt.where(Task.is_archived == archived)

    tasks = db.execute(stmt.order_by(Task.created_at.desc())).scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

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
def delete_task(task_id: int, hard: bool = False, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if hard:
        db.delete(task)
    else:
        task.is_archived = True
        db.add(task)
    db.commit()
    return None
