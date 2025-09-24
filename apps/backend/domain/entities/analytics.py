"""Analytics event domain entity."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from ..enums import EventType
from .base import TimestampedEntity


class EventLog(TimestampedEntity):
    """Analytics event log."""
    
    user_id: Optional[uuid.UUID] = None  # Anonymous events allowed
    type: EventType
    target_type: str = Field(..., min_length=1, max_length=50)  # "VENUE", "DEAL", etc.
    target_id: uuid.UUID
    session_id: Optional[str] = Field(None, max_length=100)
    
    # Event metadata
    meta: Dict[str, Any] = Field(default_factory=dict)
    
    # Device/location info
    user_agent: Optional[str] = Field(None, max_length=500)
    ip_address: Optional[str] = Field(None, max_length=45)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    
    class Config:
        from_attributes = True


class EventBatch(BaseModel):
    """Batch of events for bulk processing."""
    
    events: list[EventLog] = Field(..., min_items=1, max_items=100)
    session_id: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class AnalyticsSummary(BaseModel):
    """Analytics summary for a venue or deal."""
    
    target_id: uuid.UUID
    target_type: str
    impressions: int = 0
    clicks: int = 0
    saves: int = 0
    shares: int = 0
    calls: int = 0
    directions: int = 0
    website_visits: int = 0
    
    # Calculated metrics
    click_through_rate: float = 0.0
    save_rate: float = 0.0
    engagement_rate: float = 0.0
    
    # Time period
    period_start: datetime
    period_end: datetime
    
    class Config:
        from_attributes = True
