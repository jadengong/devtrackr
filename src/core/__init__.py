"""
Core package.

Provides configuration, database, security, and dependency injection.
"""

from .config import Config
from .database import Base, engine, SessionLocal
from .middleware import RequestTimingMiddleware, SecurityHeadersMiddleware
from .security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)
from .dependencies import (
    get_db,
    get_current_user,
    get_current_active_user,
    get_user_task,
)

__all__ = [
    # Config
    "Config",
    # Database
    "Base",
    "engine",
    "SessionLocal",
    # Middleware
    "RequestTimingMiddleware",
    "SecurityHeadersMiddleware",
    # Security
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "verify_token",
    # Dependencies
    "get_db",
    "get_current_user",
    "get_current_active_user",
    "get_user_task",
]
