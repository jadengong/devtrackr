"""
Utilities package.

Contains helper functions and utilities.
"""

from .pagination import (
    encode_cursor,
    decode_cursor,
    create_task_cursor,
    parse_task_cursor,
    get_pagination_params,
)
from .search_utils import (
    normalize_search_query,
    build_search_query,
    get_search_suggestions,
    extract_search_terms,
    calculate_search_stats,
)
from .utils import (
    generate_slug,
    format_duration,
    is_valid_email,
    get_current_timestamp,
    truncate_string,
)

__all__ = [
    # Pagination
    "encode_cursor",
    "decode_cursor",
    "create_task_cursor",
    "parse_task_cursor",
    "get_pagination_params",
    # Search
    "normalize_search_query",
    "build_search_query",
    "get_search_suggestions",
    "extract_search_terms",
    "calculate_search_stats",
    # Utils
    "generate_slug",
    "format_duration",
    "is_valid_email",
    "get_current_timestamp",
    "truncate_string",
]
