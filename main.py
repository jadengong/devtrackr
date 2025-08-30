from fastapi import FastAPI
from routers import tasks as task_router
from routers import auth as auth_router

# Create FastAPI app
app = FastAPI(
    title="DevTrackr",
    description="A Python-based backend service for task management and productivity tracking",
    version="1.0.0"
)

# Include the routers
app.include_router(auth_router.router)
app.include_router(task_router.router)

# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to DevTrackr API"}

