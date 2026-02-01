"""Activity log schemas."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ActivityLogOut(BaseModel):
    """Activity log output schema."""

    id: int
    activity_type: str
    entity_type: str
    entity_id: Optional[int]
    description: str
    activity_metadata: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityLogListResponse(BaseModel):
    """Paginated activity log response."""

    items: List[ActivityLogOut]
    next_cursor: Optional[str] = None
    has_next: bool = False
    total_count: Optional[int] = None
