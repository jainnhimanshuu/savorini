"""Event log repository implementation."""

import json
import uuid
from typing import Any, Dict, List

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import EventLog
from repositories.base import BaseRepository
from repositories.models import EventLog as EventLogModel


class EventLogRepositoryImpl(BaseRepository[EventLog, EventLogModel]):
    """Event log repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, EventLogModel)
    
    async def create_batch(self, events: List[EventLog]) -> List[EventLog]:
        """Create multiple event logs."""
        db_objects = [self._entity_to_model(event) for event in events]
        self.db.add_all(db_objects)
        await self.db.flush()
        
        # Refresh all objects to get IDs
        for obj in db_objects:
            await self.db.refresh(obj)
        
        return [self._model_to_entity(obj) for obj in db_objects]
    
    async def get_analytics_summary(
        self,
        target_id: uuid.UUID,
        target_type: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Get analytics summary for target."""
        # Get event counts by type
        result = await self.db.execute(
            select(
                EventLogModel.type,
                func.count(EventLogModel.id).label("count")
            )
            .where(
                and_(
                    EventLogModel.target_id == target_id,
                    EventLogModel.target_type == target_type,
                    EventLogModel.created_at >= start_date,
                    EventLogModel.created_at <= end_date
                )
            )
            .group_by(EventLogModel.type)
        )
        
        event_counts = {row.type: row.count for row in result}
        
        # Calculate metrics
        impressions = event_counts.get("impression", 0)
        clicks = event_counts.get("click", 0)
        saves = event_counts.get("save", 0)
        shares = event_counts.get("share", 0)
        calls = event_counts.get("call", 0)
        directions = event_counts.get("directions", 0)
        website_visits = event_counts.get("website_visit", 0)
        
        # Calculate rates
        click_through_rate = (clicks / impressions * 100) if impressions > 0 else 0
        save_rate = (saves / impressions * 100) if impressions > 0 else 0
        engagement_rate = ((clicks + saves + shares) / impressions * 100) if impressions > 0 else 0
        
        return {
            "target_id": str(target_id),
            "target_type": target_type,
            "impressions": impressions,
            "clicks": clicks,
            "saves": saves,
            "shares": shares,
            "calls": calls,
            "directions": directions,
            "website_visits": website_visits,
            "click_through_rate": round(click_through_rate, 2),
            "save_rate": round(save_rate, 2),
            "engagement_rate": round(engagement_rate, 2),
            "period_start": start_date,
            "period_end": end_date,
        }
    
    def _entity_to_model(self, entity: EventLog) -> EventLogModel:
        """Convert EventLog entity to EventLogModel."""
        return EventLogModel(
            id=entity.id,
            user_id=entity.user_id,
            type=entity.type,
            target_type=entity.target_type,
            target_id=entity.target_id,
            session_id=entity.session_id,
            ip_address=entity.ip_address,
            user_agent=entity.user_agent,
            meta=json.dumps(entity.meta) if entity.meta else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: EventLogModel) -> EventLog:
        """Convert EventLogModel to EventLog entity."""
        return EventLog(
            id=model.id,
            user_id=model.user_id,
            type=model.type,
            target_type=model.target_type,
            target_id=model.target_id,
            session_id=model.session_id,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            meta=json.loads(model.meta) if model.meta else {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
