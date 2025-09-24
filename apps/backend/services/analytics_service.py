"""Analytics service for event tracking and metrics."""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from domain.entities import EventLog, AnalyticsSummary
from domain.enums import EventType
from repositories.interfaces import EventLogRepository
from core.logging import get_logger

logger = get_logger(__name__)


class AnalyticsService:
    """Service for analytics and event tracking."""
    
    def __init__(self, event_repo: EventLogRepository):
        self.event_repo = event_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def track_event(
        self,
        event_type: EventType,
        target_type: str,
        target_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        session_id: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> EventLog:
        """Track a single event."""
        event = EventLog(
            user_id=user_id,
            type=event_type,
            target_type=target_type,
            target_id=target_id,
            session_id=session_id,
            meta=meta or {},
            ip_address=ip_address,
            user_agent=user_agent,
            latitude=latitude,
            longitude=longitude,
        )
        
        created_event = await self.event_repo.create(event)
        self.logger.debug(
            "Event tracked",
            event_type=event_type.value,
            target_type=target_type,
            target_id=str(target_id),
            user_id=str(user_id) if user_id else None
        )
        
        return created_event
    
    async def track_events_batch(self, events: List[EventLog]) -> List[EventLog]:
        """Track multiple events in batch."""
        if not events:
            return []
        
        created_events = await self.event_repo.create_batch(events)
        self.logger.info(
            "Batch events tracked",
            count=len(created_events),
            event_types=[e.type.value for e in created_events]
        )
        
        return created_events
    
    async def get_analytics_summary(
        self,
        target_id: uuid.UUID,
        target_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> AnalyticsSummary:
        """Get analytics summary for a target."""
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Convert to ISO strings
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        
        summary_data = await self.event_repo.get_analytics_summary(
            target_id, target_type, start_str, end_str
        )
        
        return AnalyticsSummary(**summary_data)
    
    async def track_impression(
        self,
        target_type: str,
        target_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> EventLog:
        """Track an impression event."""
        return await self.track_event(
            EventType.IMPRESSION,
            target_type,
            target_id,
            user_id=user_id,
            session_id=session_id,
            **kwargs
        )
    
    async def track_click(
        self,
        target_type: str,
        target_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> EventLog:
        """Track a click event."""
        return await self.track_event(
            EventType.CLICK,
            target_type,
            target_id,
            user_id=user_id,
            session_id=session_id,
            **kwargs
        )
    
    async def track_save(
        self,
        target_type: str,
        target_id: uuid.UUID,
        user_id: uuid.UUID,
        session_id: Optional[str] = None,
        **kwargs
    ) -> EventLog:
        """Track a save event."""
        return await self.track_event(
            EventType.SAVE,
            target_type,
            target_id,
            user_id=user_id,
            session_id=session_id,
            **kwargs
        )
    
    async def track_flag(
        self,
        target_type: str,
        target_id: uuid.UUID,
        user_id: uuid.UUID,
        reason: str,
        session_id: Optional[str] = None,
        **kwargs
    ) -> EventLog:
        """Track a flag event."""
        meta = kwargs.get('meta', {})
        meta['reason'] = reason
        
        return await self.track_event(
            EventType.FLAG,
            target_type,
            target_id,
            user_id=user_id,
            session_id=session_id,
            meta=meta,
            **{k: v for k, v in kwargs.items() if k != 'meta'}
        )
    
    async def get_popular_venues(
        self,
        limit: int = 10,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get popular venues based on analytics."""
        # This would typically query the analytics data
        # For now, return empty list - would need to implement in repository
        return []
    
    async def get_trending_deals(
        self,
        limit: int = 10,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get trending deals based on analytics."""
        # This would typically query the analytics data
        # For now, return empty list - would need to implement in repository
        return []
