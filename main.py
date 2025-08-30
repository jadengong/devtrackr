from fastapi import FastAPI, status, HTTPException
from datetime import datetime, timezone
from typing import Literal, Optional # Only accepts iso, seconds, for /time, 422 for anything else 
from pydantic import BaseModel, Field # Parent class for defining data model, and adding extra rules to model fields
from routers import tasks as task_router
<<<<<<< Updated upstream
=======
from routers import auth as auth_router
from routers import metrics as metrics_router
>>>>>>> Stashed changes

# Pydantic Model(s)
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[Literal["todo", "doing", "done"]] = None

# In-memory storage (temp database)
tasks: dict[list, dict] = {} 
_next_id = 1

def _reset_state_for_test():
    global tasks, _next_id
    tasks.clear()
    _next_id = 1

# Define genid to be used in create_task
def _gen_id() -> int:
    global _next_id
    i = _next_id
    _next_id += 1
    return i


# Wire router
app = FastAPI(title="DevTrackr")
app.include_router(task_router.router)
app.include_router(metrics_router.router)

# FastAPI App
app = FastAPI()

# Defining each route
@app.get("/")
def root():
    return {"status" : "ok", "message" : "Welcome to DevTrackr API"}

@app.get("/time")
def current_time(format: Literal["iso", "seconds"] = "iso"): # = "iso" is the default value
    # 1. Get the current UTC time
    now = datetime.now(timezone.utc)
    # 2. Check the format value
    
    # If format is "seconds", strip the microseconds
    if(format == "seconds"):
        now = now.replace(microsecond=0)

    # 3. Return the timestamp in the requested format as JSON
    return {"time" : now.isoformat().replace("+00:00", "Z")}

# Create an in-memory tasks list to add POST /tasks, view GET /tasks

# POST
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
# Accept JSON with title, description (optional), and sets default status to "Todo"
# Return created task with an ID
def create_task(payload: TaskCreate):
    # Create a dict named "task" that:
        # - "id" - call _gen_id()
        # - "title": payload.title
        # - "description": payload.description
        # - "category": payload.category
        # - "status": default to "todo"
        # (Optional now) "estimated_minutes" and "actual_minutes" can come later

    new_id = _gen_id()

    task = {
        "id" : new_id,
        "title" : payload.title,
        "description" : payload.description,
        "category" : payload.category,
        "status" : "todo",
    }

    tasks[new_id] = task
    return task

# GET
@app.get("/tasks")
def list_task(
    status: Optional[Literal["todo", "doing", "done"]] = None,
    category: Optional[str] = None
):

    data = list(tasks.values()) # start with all tasks

    if status:
        data = [t for t in data if t["status"] == status]

    if category:
        data = [t for t in data if t["category"] == category]

    return data

# GET, but by {id}
@app.get("/tasks/{task_id}")
def get_task(task_id : int):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# PATCH /tasks/{id} to modify 
@app.patch("/tasks/{task_id}")
def patch_task(task_id : int, payload : TaskUpdate):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail = "Task not found")

    updates = payload.model_dump(exclude_unset=True) # Since PATCH is a partial update, user might only send "status" : "doing" , basically says include fields that were actually sent in req body
    task.update(updates)
    return task

# DELETE
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id : int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail = "Task not found")
    del tasks[task_id]

    return

