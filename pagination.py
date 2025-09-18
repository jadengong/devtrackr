"""
Pagination utilities for cursor-based pagination.
"""
import base64
import json
from typing import Any, Dict, Optional, Tuple
from datetime import datetime


def encode_cursor(data: Dict[str, Any]) -> str:
    """Encode cursor data to a base64 string."""
    json_str = json.dumps(data, default=str)
    return base64.b64encode(json_str.encode()).decode()


def decode_cursor(cursor: str) -> Optional[Dict[str, Any]]:
    """Decode cursor string to data dictionary."""
    try:
        json_str = base64.b64decode(cursor.encode()).decode()
        return json.loads(json_str)
    except Exception:
        return None


def create_task_cursor(task_id: int, created_at: datetime) -> str:
    """Create a cursor for a task based on ID and creation time."""
    return encode_cursor({
        "id": task_id,
        "created_at": created_at.isoformat()
    })


def parse_task_cursor(cursor: str) -> Tuple[Optional[int], Optional[datetime]]:
    """Parse task cursor to extract ID and creation time."""
    data = decode_cursor(cursor)
    if not data:
        return None, None
    
    task_id = data.get("id")
    created_at_str = data.get("created_at")
    
    if task_id and created_at_str:
        try:
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            return task_id, created_at
        except ValueError:
            pass
    
    return None, None


def get_pagination_params(
    cursor: Optional[str] = None,
    limit: int = 20
) -> Tuple[Optional[int], Optional[datetime], int]:
    """
    Parse pagination parameters.
    
    Returns:
        Tuple of (cursor_id, cursor_created_at, limit)
    """
    if limit > 100:
        limit = 100  # Cap at 100 items per page
    
    cursor_id, cursor_created_at = None, None
    if cursor:
        cursor_id, cursor_created_at = parse_task_cursor(cursor)
    
    return cursor_id, cursor_created_at, limit
