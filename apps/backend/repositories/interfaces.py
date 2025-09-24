"""Repository interfaces following the Repository pattern."""

import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from domain.entities import (
    Deal,
    EventLog,
    Favorite,
    Flag,
    Media,
    ProvinceRule,
    User,
    Venue,
    VenueWithDetails,
)


class UserRepository(Protocol):
    """User repository interface."""
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        ...
    
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID."""
        ...
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        ...
    
    async def update(self, user: User) -> User:
        """Update user."""
        ...
    
    async def delete(self, user_id: uuid.UUID) -> bool:
        """Delete user."""
        ...
    
    async def list_by_role(self, role: str, limit: int = 100, offset: int = 0) -> List[User]:
        """List users by role."""
        ...


class VenueRepository(Protocol):
    """Venue repository interface."""
    
    async def create(self, venue: Venue) -> Venue:
        """Create a new venue."""
        ...
    
    async def get_by_id(self, venue_id: uuid.UUID) -> Optional[VenueWithDetails]:
        """Get venue by ID with details."""
        ...
    
    async def get_by_slug(self, slug: str) -> Optional[VenueWithDetails]:
        """Get venue by slug."""
        ...
    
    async def update(self, venue: Venue) -> Venue:
        """Update venue."""
        ...
    
    async def delete(self, venue_id: uuid.UUID) -> bool:
        """Delete venue."""
        ...
    
    async def list_by_vendor(self, vendor_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Venue]:
        """List venues by vendor."""
        ...
    
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        limit: int = 50,
        offset: int = 0
    ) -> List[VenueWithDetails]:
        """Search venues near coordinates."""
        ...
    
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
        ...


class DealRepository(Protocol):
    """Deal repository interface."""
    
    async def create(self, deal: Deal) -> Deal:
        """Create a new deal."""
        ...
    
    async def get_by_id(self, deal_id: uuid.UUID) -> Optional[Deal]:
        """Get deal by ID."""
        ...
    
    async def update(self, deal: Deal) -> Deal:
        """Update deal."""
        ...
    
    async def delete(self, deal_id: uuid.UUID) -> bool:
        """Delete deal."""
        ...
    
    async def list_by_venue(self, venue_id: uuid.UUID, active_only: bool = True) -> List[Deal]:
        """List deals by venue."""
        ...
    
    async def list_active_nearby(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Deal]:
        """List active deals nearby."""
        ...
    
    async def list_featured(self, limit: int = 20) -> List[Deal]:
        """List featured deals."""
        ...


class MediaRepository(Protocol):
    """Media repository interface."""
    
    async def create(self, media: Media) -> Media:
        """Create new media."""
        ...
    
    async def get_by_id(self, media_id: uuid.UUID) -> Optional[Media]:
        """Get media by ID."""
        ...
    
    async def list_by_venue(self, venue_id: uuid.UUID, media_type: Optional[str] = None) -> List[Media]:
        """List media by venue."""
        ...
    
    async def update(self, media: Media) -> Media:
        """Update media."""
        ...
    
    async def delete(self, media_id: uuid.UUID) -> bool:
        """Delete media."""
        ...


class FavoriteRepository(Protocol):
    """Favorite repository interface."""
    
    async def create(self, favorite: Favorite) -> Favorite:
        """Create a favorite."""
        ...
    
    async def get_by_user_and_venue(self, user_id: uuid.UUID, venue_id: uuid.UUID) -> Optional[Favorite]:
        """Get favorite by user and venue."""
        ...
    
    async def list_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Favorite]:
        """List favorites by user."""
        ...
    
    async def delete(self, favorite_id: uuid.UUID) -> bool:
        """Delete favorite."""
        ...


class FlagRepository(Protocol):
    """Flag repository interface."""
    
    async def create(self, flag: Flag) -> Flag:
        """Create a flag."""
        ...
    
    async def get_by_id(self, flag_id: uuid.UUID) -> Optional[Flag]:
        """Get flag by ID."""
        ...
    
    async def list_pending(self, limit: int = 50, offset: int = 0) -> List[Flag]:
        """List pending flags."""
        ...
    
    async def update(self, flag: Flag) -> Flag:
        """Update flag."""
        ...


class ProvinceRuleRepository(Protocol):
    """Province rule repository interface."""
    
    async def get_by_province(self, province: str) -> Optional[ProvinceRule]:
        """Get province rule by province."""
        ...
    
    async def list_all(self) -> List[ProvinceRule]:
        """List all province rules."""
        ...
    
    async def update(self, rule: ProvinceRule) -> ProvinceRule:
        """Update province rule."""
        ...


class EventLogRepository(Protocol):
    """Event log repository interface."""
    
    async def create(self, event: EventLog) -> EventLog:
        """Create event log."""
        ...
    
    async def create_batch(self, events: List[EventLog]) -> List[EventLog]:
        """Create multiple event logs."""
        ...
    
    async def get_analytics_summary(
        self,
        target_id: uuid.UUID,
        target_type: str,
        start_date: str,
        end_date: str
    ) -> dict:
        """Get analytics summary for target."""
        ...
