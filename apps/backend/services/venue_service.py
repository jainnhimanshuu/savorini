"""Venue service for business logic."""

import uuid
from typing import List, Optional

from domain.entities import Venue, VenueWithDetails
from domain.enums import Province, VenueStatus
from repositories.interfaces import VenueRepository
from core.exceptions import BusinessRuleError, NotFoundError
from core.logging import get_logger

logger = get_logger(__name__)


class VenueService:
    """Service for venue business logic."""
    
    def __init__(self, venue_repo: VenueRepository):
        self.venue_repo = venue_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def create_venue(self, venue: Venue) -> Venue:
        """Create a new venue."""
        # Validate business rules
        await self._validate_venue_creation(venue)
        
        # Generate slug if not provided
        if not venue.slug:
            venue.slug = self._generate_slug(venue.name)
        
        # Set default status
        venue.status = VenueStatus.PENDING
        
        created_venue = await self.venue_repo.create(venue)
        self.logger.info("Venue created", venue_id=str(created_venue.id), name=created_venue.name)
        
        return created_venue
    
    async def get_venue(self, venue_id: uuid.UUID) -> VenueWithDetails:
        """Get venue by ID with details."""
        venue = await self.venue_repo.get_by_id(venue_id)
        if not venue:
            raise NotFoundError(f"Venue with id {venue_id} not found")
        
        return venue
    
    async def get_venue_by_slug(self, slug: str) -> VenueWithDetails:
        """Get venue by slug."""
        venue = await self.venue_repo.get_by_slug(slug)
        if not venue:
            raise NotFoundError(f"Venue with slug {slug} not found")
        
        return venue
    
    async def update_venue(self, venue: Venue) -> Venue:
        """Update venue."""
        # Validate business rules
        await self._validate_venue_update(venue)
        
        updated_venue = await self.venue_repo.update(venue)
        self.logger.info("Venue updated", venue_id=str(updated_venue.id))
        
        return updated_venue
    
    async def delete_venue(self, venue_id: uuid.UUID) -> bool:
        """Delete venue."""
        success = await self.venue_repo.delete(venue_id)
        if success:
            self.logger.info("Venue deleted", venue_id=str(venue_id))
        else:
            self.logger.warning("Failed to delete venue", venue_id=str(venue_id))
        
        return success
    
    async def list_vendor_venues(self, vendor_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Venue]:
        """List venues by vendor."""
        return await self.venue_repo.list_by_vendor(vendor_id, limit, offset)
    
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        limit: int = 50,
        offset: int = 0
    ) -> List[VenueWithDetails]:
        """Search venues near coordinates."""
        return await self.venue_repo.search_nearby(lat, lng, radius_km, limit, offset)
    
    async def search_venues(
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
        return await self.venue_repo.search_by_filters(
            query, city, province, license_type, status, limit, offset
        )
    
    async def activate_venue(self, venue_id: uuid.UUID) -> Venue:
        """Activate a venue."""
        venue = await self.venue_repo.get_by_id(venue_id)
        if not venue:
            raise NotFoundError(f"Venue with id {venue_id} not found")
        
        venue.venue.activate()
        updated_venue = await self.venue_repo.update(venue.venue)
        
        self.logger.info("Venue activated", venue_id=str(venue_id))
        return updated_venue
    
    async def suspend_venue(self, venue_id: uuid.UUID) -> Venue:
        """Suspend a venue."""
        venue = await self.venue_repo.get_by_id(venue_id)
        if not venue:
            raise NotFoundError(f"Venue with id {venue_id} not found")
        
        venue.venue.suspend()
        updated_venue = await self.venue_repo.update(venue.venue)
        
        self.logger.info("Venue suspended", venue_id=str(venue_id))
        return updated_venue
    
    async def verify_venue(self, venue_id: uuid.UUID) -> Venue:
        """Mark venue as verified."""
        venue = await self.venue_repo.get_by_id(venue_id)
        if not venue:
            raise NotFoundError(f"Venue with id {venue_id} not found")
        
        venue.venue.verify()
        updated_venue = await self.venue_repo.update(venue.venue)
        
        self.logger.info("Venue verified", venue_id=str(venue_id))
        return updated_venue
    
    async def _validate_venue_creation(self, venue: Venue) -> None:
        """Validate venue creation business rules."""
        # Check if vendor already has a venue with the same name
        existing_venues = await self.venue_repo.list_by_vendor(venue.vendor_id, limit=1000)
        for existing in existing_venues:
            if existing.name.lower() == venue.name.lower():
                raise BusinessRuleError(
                    f"Vendor already has a venue named '{venue.name}'",
                    code="DUPLICATE_VENUE_NAME"
                )
        
        # Validate province is supported
        if venue.province not in [Province.ON, Province.BC, Province.AB]:
            raise BusinessRuleError(
                f"Province {venue.province.value} is not yet supported",
                code="UNSUPPORTED_PROVINCE"
            )
    
    async def _validate_venue_update(self, venue: Venue) -> None:
        """Validate venue update business rules."""
        # Check if venue exists
        existing = await self.venue_repo.get_by_id(venue.id)
        if not existing:
            raise NotFoundError(f"Venue with id {venue.id} not found")
    
    def _generate_slug(self, name: str) -> str:
        """Generate URL-friendly slug from venue name."""
        import re
        
        # Convert to lowercase and replace spaces with hyphens
        slug = name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special characters
        slug = re.sub(r'[-\s]+', '-', slug)   # Replace spaces and multiple hyphens
        slug = slug.strip('-')                # Remove leading/trailing hyphens
        
        return slug
