"""
Utility functions and modules for DevTrackr.

This package contains various utility modules:
- pagination: Cursor-based pagination utilities
- search_utils: Full-text search utilities
- utils: General utility functions
"""

from .pagination import *
from .search_utils import *
from .utils import *

__all__ = [
    # Pagination exports
    "create_task_cursor",
    "get_pagination_params",
    # Search utilities exports
    "build_search_query",
    "get_search_suggestions",
    "normalize_search_query",
    "calculate_search_stats",
    # General utilities exports
    "generate_slug",
    "format_duration",
    "is_valid_email",
    "get_current_timestamp",
    "truncate_string",
]
