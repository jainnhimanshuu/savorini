"""Search service for feed and discovery."""

import uuid
from typing import List, Optional

from domain.entities import Deal, DealWithVenue, VenueWithDetails
from repositories.interfaces import DealRepository, VenueRepository
from core.logging import get_logger

logger = get_logger(__name__)


class SearchService:
    """Service for search and discovery functionality."""
    
    def __init__(self, venue_repo: VenueRepository, deal_repo: DealRepository):
        self.venue_repo = venue_repo
        self.deal_repo = deal_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def search_venues(
        self,
        query: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        license_type: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[VenueWithDetails]:
        """Search venues with various filters."""
        # If coordinates provided, use geo search
        if lat is not None and lng is not None:
            radius = radius_km or 10.0
            return await self.venue_repo.search_nearby(lat, lng, radius, limit, offset)
        
        # Otherwise use filter-based search
        return await self.venue_repo.search_by_filters(
            query, city, province, license_type, None, limit, offset
        )
    
    async def search_deals(
        self,
        venue_id: Optional[uuid.UUID] = None,
        category: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_km: Optional[float] = None,
        active_only: bool = True,
        featured_only: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> List[Deal]:
        """Search deals with various filters."""
        # If coordinates provided, use geo search
        if lat is not None and lng is not None:
            radius = radius_km or 10.0
            return await self.deal_repo.list_active_nearby(lat, lng, radius, category, limit, offset)
        
        # If venue specified, get deals for that venue
        if venue_id:
            return await self.deal_repo.list_by_venue(venue_id, active_only)
        
        # If featured only, get featured deals
        if featured_only:
            return await self.deal_repo.list_featured(limit)
        
        # Default: return empty list (need more specific filters)
        return []
    
    async def get_feed_items(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        when: str = "now",
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[DealWithVenue]:
        """Get feed items for discovery."""
        # Get nearby deals
        deals = await self.deal_repo.list_active_nearby(
            lat, lng, radius_km, category, limit, offset
        )
        
        # Convert to DealWithVenue format
        feed_items = []
        for deal in deals:
            # Get venue details for each deal
            venue = await self.venue_repo.get_by_id(deal.venue_id)
            if venue:
                feed_item = DealWithVenue(
                    deal=deal,
                    venue_name=venue.venue.name,
                    venue_address=venue.venue.address,
                    venue_city=venue.venue.city,
                    venue_province=venue.venue.province.value,
                    distance_km=venue.distance_km,
                    savings_amount=deal.savings_amount,
                    savings_percentage=deal.savings_percentage,
                )
                feed_items.append(feed_item)
        
        return feed_items
    
    async def get_trending_deals(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        limit: int = 20
    ) -> List[DealWithVenue]:
        """Get trending deals (featured + popular)."""
        # Get featured deals first
        featured_deals = await self.deal_repo.list_featured(limit // 2)
        
        # Get popular deals (could be based on analytics in the future)
        popular_deals = await self.deal_repo.list_active_nearby(
            lat, lng, radius_km, None, limit // 2
        )
        
        # Combine and deduplicate
        all_deals = featured_deals + popular_deals
        unique_deals = {deal.id: deal for deal in all_deals}.values()
        
        # Convert to DealWithVenue format
        trending_items = []
        for deal in list(unique_deals)[:limit]:
            venue = await self.venue_repo.get_by_id(deal.venue_id)
            if venue:
                feed_item = DealWithVenue(
                    deal=deal,
                    venue_name=venue.venue.name,
                    venue_address=venue.venue.address,
                    venue_city=venue.venue.city,
                    venue_province=venue.venue.province.value,
                    distance_km=venue.distance_km,
                    savings_amount=deal.savings_amount,
                    savings_percentage=deal.savings_percentage,
                )
                trending_items.append(feed_item)
        
        return trending_items
