from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import logging
from routers import tasks as task_router
from routers import auth as auth_router
from routers import metrics as metrics_router
from routers import time_tracking as time_router
from datetime import datetime, timezone

# Create FastAPI app
app = FastAPI(title="DevTrackr")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Centralized API version
API_VERSION = "1.0.2"

# Include routers
app.include_router(task_router.router)
app.include_router(auth_router.router)
app.include_router(metrics_router.router)
app.include_router(time_router.router)

# Track application start time for readiness metrics
START_TIME = datetime.now(timezone.utc)

# Configure CORS via env: CORS_ORIGINS=domain1,domain2 or "*"
_origins_env = os.getenv("CORS_ORIGINS", "*")
ALLOWED_ORIGINS = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ALLOWED_ORIGINS == ["*"] else ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    logger.info(f"Request {request_id}: {response.status_code}")
    return response


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
        "version": API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Lightweight liveness probe
@app.get("/live")
def liveness_probe():
    return {"status": "ok"}


# Readiness probe with simple uptime metric
@app.get("/ready")
def readiness_probe():
    uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
    return {
        "status": "ready",
        "uptime_seconds": uptime_seconds,
    }


# Version endpoint
@app.get("/version")
def version():
    return {"version": API_VERSION}
