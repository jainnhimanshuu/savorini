"""Venue repository implementation."""

import uuid
from typing import List, Optional

from geoalchemy2 import WKTElement
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Venue, VenueWithDetails
from domain.enums import LicenseType, Province, VenueStatus
from repositories.base import BaseRepository
from repositories.models import (
    Deal as DealModel,
    Hours as HoursModel,
    Media as MediaModel,
    SecondaryHours as SecondaryHoursModel,
    Venue as VenueModel,
)


class VenueRepositoryImpl(BaseRepository[Venue, VenueModel]):
    """Venue repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, VenueModel)
    
    async def get_by_id(self, venue_id: uuid.UUID) -> Optional[VenueWithDetails]:
        """Get venue by ID with details."""
        result = await self.db.execute(
            select(VenueModel)
            .options(
                selectinload(VenueModel.hours),
                selectinload(VenueModel.secondary_hours),
                selectinload(VenueModel.media),
            )
            .where(VenueModel.id == venue_id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        # Get deals count
        deals_count_result = await self.db.execute(
            select(func.count(DealModel.id))
            .where(and_(DealModel.venue_id == venue_id, DealModel.is_active == True))
        )
        deals_count = deals_count_result.scalar() or 0
        
        return self._model_to_venue_with_details(db_obj, deals_count)
    
    async def get_by_slug(self, slug: str) -> Optional[VenueWithDetails]:
        """Get venue by slug."""
        result = await self.db.execute(
            select(VenueModel)
            .options(
                selectinload(VenueModel.hours),
                selectinload(VenueModel.secondary_hours),
                selectinload(VenueModel.media),
            )
            .where(VenueModel.slug == slug)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        # Get deals count
        deals_count_result = await self.db.execute(
            select(func.count(DealModel.id))
            .where(and_(DealModel.venue_id == db_obj.id, DealModel.is_active == True))
        )
        deals_count = deals_count_result.scalar() or 0
        
        return self._model_to_venue_with_details(db_obj, deals_count)
    
    async def list_by_vendor(self, vendor_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Venue]:
        """List venues by vendor."""
        result = await self.db.execute(
            select(VenueModel)
            .where(VenueModel.vendor_id == vendor_id)
            .offset(offset)
            .limit(limit)
            .order_by(VenueModel.created_at.desc())
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        limit: int = 50,
        offset: int = 0
    ) -> List[VenueWithDetails]:
        """Search venues near coordinates using PostGIS."""
        # Create point from coordinates
        point = WKTElement(f"POINT({lng} {lat})", srid=4326)
        
        # Calculate distance and filter by radius
        result = await self.db.execute(
            select(
                VenueModel,
                func.ST_Distance(VenueModel.geo, point).label("distance")
            )
            .options(
                selectinload(VenueModel.hours),
                selectinload(VenueModel.secondary_hours),
                selectinload(VenueModel.media),
            )
            .where(
                and_(
                    VenueModel.geo.isnot(None),
                    func.ST_DWithin(
                        VenueModel.geo,
                        point,
                        radius_km * 1000  # Convert km to meters
                    )
                )
            )
            .order_by("distance")
            .offset(offset)
            .limit(limit)
        )
        
        venues_with_distance = result.all()
        venues_with_details = []
        
        for venue_model, distance in venues_with_distance:
            # Get deals count
            deals_count_result = await self.db.execute(
                select(func.count(DealModel.id))
                .where(and_(DealModel.venue_id == venue_model.id, DealModel.is_active == True))
            )
            deals_count = deals_count_result.scalar() or 0
            
            venue_details = self._model_to_venue_with_details(venue_model, deals_count)
            venue_details.distance_km = distance / 1000  # Convert meters to km
            venues_with_details.append(venue_details)
        
        return venues_with_details
    
    async def search_by_filters(
        self,
        query: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        license_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[VenueWithDetails]:
        """Search venues by filters."""
        stmt = select(VenueModel).options(
            selectinload(VenueModel.hours),
            selectinload(VenueModel.secondary_hours),
            selectinload(VenueModel.media),
        )
        
        conditions = []
        
        if query:
            conditions.append(
                or_(
                    VenueModel.name.ilike(f"%{query}%"),
                    VenueModel.description.ilike(f"%{query}%"),
                    VenueModel.address.ilike(f"%{query}%")
                )
            )
        
        if city:
            conditions.append(VenueModel.city.ilike(f"%{city}%"))
        
        if province:
            conditions.append(VenueModel.province == Province(province))
        
        if license_type:
            conditions.append(VenueModel.license_type == LicenseType(license_type))
        
        if status:
            conditions.append(VenueModel.status == VenueStatus(status))
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(offset).limit(limit).order_by(VenueModel.created_at.desc())
        
        result = await self.db.execute(stmt)
        db_objects = result.scalars().all()
        
        venues_with_details = []
        for venue_model in db_objects:
            # Get deals count
            deals_count_result = await self.db.execute(
                select(func.count(DealModel.id))
                .where(and_(DealModel.venue_id == venue_model.id, DealModel.is_active == True))
            )
            deals_count = deals_count_result.scalar() or 0
            
            venues_with_details.append(self._model_to_venue_with_details(venue_model, deals_count))
        
        return venues_with_details
    
    def _entity_to_model(self, entity: Venue) -> VenueModel:
        """Convert Venue entity to VenueModel."""
        return VenueModel(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            description=entity.description,
            address=entity.address,
            city=entity.city,
            province=entity.province,
            postal_code=entity.postal_code,
            geo=entity.geo,
            phone=entity.phone,
            email=entity.email,
            website=entity.website,
            license_type=entity.license_type,
            vendor_id=entity.vendor_id,
            status=entity.status,
            has_patio=entity.has_patio,
            has_parking=entity.has_parking,
            has_wifi=entity.has_wifi,
            is_accessible=entity.is_accessible,
            google_place_id=entity.google_place_id,
            last_verified_at=entity.last_verified_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: VenueModel) -> Venue:
        """Convert VenueModel to Venue entity."""
        return Venue(
            id=model.id,
            name=model.name,
            slug=model.slug,
            description=model.description,
            address=model.address,
            city=model.city,
            province=model.province,
            postal_code=model.postal_code,
            geo=model.geo,
            phone=model.phone,
            email=model.email,
            website=model.website,
            license_type=model.license_type,
            vendor_id=model.vendor_id,
            status=model.status,
            has_patio=model.has_patio,
            has_parking=model.has_parking,
            has_wifi=model.has_wifi,
            is_accessible=model.is_accessible,
            google_place_id=model.google_place_id,
            last_verified_at=model.last_verified_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _model_to_venue_with_details(self, model: VenueModel, deals_count: int) -> VenueWithDetails:
        """Convert VenueModel to VenueWithDetails."""
        from domain.entities import Hours, SecondaryHours
        
        # Convert hours
        hours = [
            Hours(
                venue_id=h.venue_id,
                day=h.day,
                open_time=h.open_time,
                close_time=h.close_time,
                is_closed=h.is_closed,
            )
            for h in model.hours
        ]
        
        # Convert secondary hours
        secondary_hours = [
            SecondaryHours(
                venue_id=sh.venue_id,
                type=sh.type,
                day=sh.day,
                start_time=sh.start_time,
                end_time=sh.end_time,
                is_active=sh.is_active,
            )
            for sh in model.secondary_hours
        ]
        
        return VenueWithDetails(
            venue=self._model_to_entity(model),
            hours=hours,
            secondary_hours=secondary_hours,
            deals_count=deals_count,
        )
