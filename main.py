from fastapi import FastAPI
from routers import tasks as task_router
from routers import auth as auth_router
from routers import metrics as metrics_router
from routers import time_tracking as time_router
from datetime import datetime, timezone

# Create FastAPI app
app = FastAPI(title="DevTrackr")

# Include routers
app.include_router(task_router.router)
app.include_router(auth_router.router)
app.include_router(metrics_router.router)
app.include_router(time_router.router)


# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to DevTrackr API"}


# Health check endpoint for Docker and monitoring
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DevTrackr API",
        "version": "1.0.2",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
