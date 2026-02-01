"""
Routes package.

Contains all API route definitions.
"""

from . import auth
from . import tasks
from . import metrics
from . import time_tracking
from . import activity

__all__ = [
    "auth",
    "tasks",
    "metrics",
    "time_tracking",
    "activity",
]
