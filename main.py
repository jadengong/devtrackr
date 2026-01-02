from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uuid
import logging
from routers import tasks as task_router
from routers import auth as auth_router
from routers import metrics as metrics_router
from routers import time_tracking as time_router
from routers import activity as activity_router
from datetime import datetime, timezone
from config import Config
from config.middleware import RequestTimingMiddleware, SecurityHeadersMiddleware

# Create FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
)

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Use config for API version
API_VERSION = Config.API_VERSION


# Custom exception classes
class DevTrackrException(Exception):
    """Base exception for DevTrackr application"""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(DevTrackrException):
    """Raised when validation fails"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, 400, details)


class NotFoundError(DevTrackrException):
    """Raised when a resource is not found"""

    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, 404, details)


class UnauthorizedError(DevTrackrException):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Unauthorized", details: dict = None):
        super().__init__(message, 401, details)


class ForbiddenError(DevTrackrException):
    """Raised when access is forbidden"""

    def __init__(self, message: str = "Forbidden", details: dict = None):
        super().__init__(message, 403, details)


# Include routers
app.include_router(task_router.router)
app.include_router(auth_router.router)
app.include_router(metrics_router.router)
app.include_router(time_router.router)
app.include_router(activity_router.router)

# Track application start time for readiness metrics
START_TIME = datetime.now(timezone.utc)

# Add custom middleware
app.add_middleware(RequestTimingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(DevTrackrException)
async def devtrackr_exception_handler(request: Request, exc: DevTrackrException):
    """Handle custom DevTrackr exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Request {request_id}: DevTrackr error - {exc.message}", exc_info=True
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Request {request_id}: HTTP error {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "status_code": exc.status_code,
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Request {request_id}: Validation error - {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "error": {
                "type": "ValidationError",
                "message": "Request validation failed",
                "details": exc.errors(),
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Request {request_id}: Unexpected error - {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
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
    return {
        "status": "ok",
        "message": "Welcome to DevTrackr API",
        "version": API_VERSION,
        "docs": "/docs",
    }


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


# Informational endpoint
@app.get("/info")
def info():
    """Basic runtime and configuration info (non-sensitive)."""
    uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
    return {
        "service": Config.API_TITLE,
        "version": API_VERSION,
        "environment": "production" if Config.is_production() else "development",
        "features": {
            "metrics": Config.ENABLE_METRICS,
            "time_tracking": Config.ENABLE_TIME_TRACKING,
        },
        "uptime_seconds": uptime_seconds,
    }


@app.post("/admin/migrate")
async def run_migrations():
    """
    Run database migrations.
    WARNING: Only use this in development or with proper authentication.
    """
    try:
        import subprocess

        # Check if running in production
        if Config.is_production():
            raise HTTPException(
                status_code=403, detail="Migration endpoint disabled in production"
            )

        # Run migrations
        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True
        )

        if result.returncode == 0:
            return {
                "message": "Database migrations completed successfully",
                "output": result.stdout,
                "timestamp": datetime.now(timezone.utc),
            }
        else:
            raise HTTPException(
                status_code=500, detail=f"Migration failed: {result.stderr}"
            )

    except Exception as e:
        logger.error(f"Migration error: {e}")
        raise HTTPException(status_code=500, detail=f"Migration error: {str(e)}")
