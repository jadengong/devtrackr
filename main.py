"""
DevTrackr API - Main application entry point.

FastAPI application with routing, middleware, and error handling.
Provides task management, time tracking, and analytics endpoints.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from uuid import uuid4
import logging
from collections import defaultdict
from routers import tasks as task_router
from routers import auth as auth_router
from routers import metrics as metrics_router
from routers import time_tracking as time_router
from routers import activity as activity_router
from datetime import datetime, timezone
from config import Config
from config.middleware import RequestTimingMiddleware, SecurityHeadersMiddleware
from core.db import engine
from sqlalchemy import text

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


class ConflictError(DevTrackrException):
    """Raised when a resource conflict occurs (e.g., duplicate entry)"""

    def __init__(self, message: str = "Resource conflict", details: dict = None):
        super().__init__(message, 409, details)


# Include routers
app.include_router(task_router.router)
app.include_router(auth_router.router)
app.include_router(metrics_router.router)
app.include_router(time_router.router)
app.include_router(activity_router.router)

# Track application start time for readiness metrics
START_TIME = datetime.now(timezone.utc)

# Track request statistics
request_stats = {
    "total_requests": 0,
    "requests_by_method": defaultdict(int),
    "requests_by_status": defaultdict(int),
    "requests_by_path": defaultdict(int),
}

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


# Helper function for standardized error responses
def create_error_response(
    exc_type: str,
    message: str,
    status_code: int,
    request_id: str,
    details: dict = None
) -> JSONResponse:
    """Create a standardized JSON error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": message,
            "error": {
                "type": exc_type,
                "message": message,
                "details": details or {},
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


# Global exception handlers
@app.exception_handler(DevTrackrException)
async def devtrackr_exception_handler(request: Request, exc: DevTrackrException):
    """Handle custom DevTrackr exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Request {request_id}: DevTrackr error - {exc.message} | Path: {request.url.path}", exc_info=True
    )

    return create_error_response(
        exc.__class__.__name__,
        exc.message,
        exc.status_code,
        request_id,
        exc.details
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Request {request_id}: HTTP error {exc.status_code} - {exc.detail} | Path: {request.url.path}")

    return create_error_response(
        "HTTPException",
        exc.detail,
        exc.status_code,
        request_id,
        {"status_code": exc.status_code}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Request {request_id}: Validation error - {exc.errors()} | Path: {request.url.path}")

    return create_error_response(
        "ValidationError",
        "Request validation failed",
        422,
        request_id,
        {"validation_errors": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Request {request_id}: Unexpected error - {str(exc)} | Path: {request.url.path}", exc_info=True)

    return create_error_response(
        "InternalServerError",
        "An unexpected error occurred",
        500,
        request_id
    )


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = uuid4().hex[:8]
    request.state.request_id = request_id

    logger.info(f"Request {request_id}: {request.method} {request.url}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    # Update request statistics
    request_stats["total_requests"] += 1
    request_stats["requests_by_method"][request.method] += 1
    request_stats["requests_by_status"][response.status_code] += 1
    request_stats["requests_by_path"][request.url.path] += 1

    logger.info(f"Request {request_id}: {response.status_code}")
    return response


# Root endpoint
@app.get("/")
def root():
    """Root endpoint providing API information and links to documentation."""
    return {
        "status": "ok",
        "message": "Welcome to DevTrackr API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.now(timezone.utc).isoformat(),
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Version endpoint
@app.get("/version")
def version():
    return {"version": API_VERSION}


# Request statistics endpoint
@app.get("/stats")
def get_stats():
    """
    Get API request statistics since application start.
    Provides insights into API usage patterns.
    """
    return {
        "total_requests": request_stats["total_requests"],
        "requests_by_method": dict(request_stats["requests_by_method"]),
        "requests_by_status": dict(request_stats["requests_by_status"]),
        "top_paths": dict(
            sorted(
                request_stats["requests_by_path"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        ),
        "uptime_seconds": int((datetime.now(timezone.utc) - START_TIME).total_seconds()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


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


# Comprehensive status endpoint with health checks
@app.get("/status")
def status():
    """
    Comprehensive status endpoint with database connectivity check.
    Useful for monitoring and orchestration systems.
    """
    uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())
    status_data = {
        "status": "healthy",
        "service": Config.API_TITLE,
        "version": API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime_seconds,
        "environment": "production" if Config.is_production() else "development",
        "checks": {
            "api": "ok",
            "database": "unknown",
        },
    }

    # Check database connectivity
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            status_data["checks"]["database"] = "ok"
    except Exception as e:
        status_data["status"] = "degraded"
        status_data["checks"]["database"] = "error"
        status_data["database_error"] = str(e)
        logger.warning(f"Database connectivity check failed: {e}")

    # Determine overall status
    if status_data["checks"]["database"] != "ok":
        status_data["status"] = "degraded"

    return status_data


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
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        else:
            raise HTTPException(
                status_code=500, detail=f"Migration failed: {result.stderr}"
            )

    except Exception as e:
        logger.error(f"Migration error: {e}")
        raise HTTPException(status_code=500, detail=f"Migration error: {str(e)}")
