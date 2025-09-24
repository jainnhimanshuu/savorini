"""Deal repository implementation."""

import uuid
from typing import List, Optional

from geoalchemy2 import WKTElement
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Deal
from domain.enums import DealCategory
from repositories.base import BaseRepository
from repositories.models import Deal as DealModel, Venue as VenueModel


class DealRepositoryImpl(BaseRepository[Deal, DealModel]):
    """Deal repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, DealModel)
    
    async def list_by_venue(self, venue_id: uuid.UUID, active_only: bool = True) -> List[Deal]:
        """List deals by venue."""
        conditions = [DealModel.venue_id == venue_id]
        if active_only:
            conditions.append(DealModel.is_active == True)
        
        result = await self.db.execute(
            select(DealModel)
            .where(and_(*conditions))
            .order_by(DealModel.created_at.desc())
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    async def list_active_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Deal]:
        """List active deals nearby using PostGIS."""
        # Create point from coordinates
        point = WKTElement(f"POINT({lng} {lat})", srid=4326)
        
        conditions = [
            DealModel.is_active == True,
            VenueModel.geo.isnot(None),
            func.ST_DWithin(
                VenueModel.geo,
                point,
                radius_km * 1000  # Convert km to meters
            )
        ]
        
        if category:
            conditions.append(DealModel.category == DealCategory(category))
        
        result = await self.db.execute(
            select(DealModel)
            .join(VenueModel, DealModel.venue_id == VenueModel.id)
            .where(and_(*conditions))
            .order_by(func.ST_Distance(VenueModel.geo, point))
            .offset(offset)
            .limit(limit)
        )
        
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    async def list_featured(self, limit: int = 20) -> List[Deal]:
        """List featured deals."""
        result = await self.db.execute(
            select(DealModel)
            .where(and_(DealModel.is_active == True, DealModel.is_featured == True))
            .order_by(DealModel.created_at.desc())
            .limit(limit)
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: Deal) -> DealModel:
        """Convert Deal entity to DealModel."""
        return DealModel(
            id=entity.id,
            venue_id=entity.venue_id,
            title=entity.title,
            description=entity.description,
            category=entity.category,
            original_price=entity.original_price,
            deal_price=entity.deal_price,
            price_display_mode=entity.price_display_mode,
            days_mask=entity.days_mask,
            start_time=entity.start_time,
            end_time=entity.end_time,
            restrictions=entity.restrictions,
            terms=entity.terms,
            min_purchase=entity.min_purchase,
            max_redemptions=entity.max_redemptions,
            redemptions_used=entity.redemptions_used,
            is_active=entity.is_active,
            is_featured=entity.is_featured,
            requires_age_verification=entity.requires_age_verification,
            last_verified_at=entity.last_verified_at,
            verified_by=entity.verified_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: DealModel) -> Deal:
        """Convert DealModel to Deal entity."""
        return Deal(
            id=model.id,
            venue_id=model.venue_id,
            title=model.title,
            description=model.description,
            category=model.category,
            original_price=model.original_price,
            deal_price=model.deal_price,
            price_display_mode=model.price_display_mode,
            days_mask=model.days_mask,
            start_time=model.start_time,
            end_time=model.end_time,
            restrictions=model.restrictions,
            terms=model.terms,
            min_purchase=model.min_purchase,
            max_redemptions=model.max_redemptions,
            redemptions_used=model.redemptions_used,
            is_active=model.is_active,
            is_featured=model.is_featured,
            requires_age_verification=model.requires_age_verification,
            last_verified_at=model.last_verified_at,
            verified_by=model.verified_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
