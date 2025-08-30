from fastapi import FastAPI
from routers import tasks as task_router

# Create FastAPI app
app = FastAPI(title="DevTrackr")

# Include the tasks router
app.include_router(task_router.router)

# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to DevTrackr API"}

