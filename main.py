from fastapi import FastAPI, status, HTTPException
from datetime import datetime, timezone
from typing import Literal, Optional # Only accepts iso, seconds, for /time, 422 for anything else 
from pydantic import BaseModel, Field # Parent class for defining data model, and adding extra rules to model fields

# Pydantic Model(s)
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None

# In-memory storage (temp database)
tasks: list[dict] = []
_next_id = 1

# Define genid to be used in create_task
def _gen_id() -> int:
    global _next_id
    i = _next_id
    _next_id += 1
    return i

# FastAPI App
app = FastAPI()

# Defining each route
@app.get("/")
def root():
    return {"status" : "ok", "message" : "Welcome to DevTrackr API"}

@app.get("/hello")
def hello():
    return {"msg": "Hello world"}

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

    tasks.append(task)
    return task

# GET
@app.get("/tasks", status_code=status.HTTP_202_ACCEPTED)
def list_task():
    return tasks

# GET, but by {id}
@app.get("/tasks/{task_id}")
def get_task(task_id : int):
    # Loop through tasks, if find task with id == task_id, return it, otherwise raise HTTPException (404)
    for t in tasks:
        if(task_id == t["id"]):
            return t
    
    raise HTTPException(status_code=404, detail="Task not found")

