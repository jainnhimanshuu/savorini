"""Deal service for business logic."""

import uuid
from typing import List, Optional

from domain.entities import Deal
from domain.enums import DealCategory, DayOfWeek
from repositories.interfaces import DealRepository
from core.exceptions import BusinessRuleError, NotFoundError
from core.logging import get_logger

logger = get_logger(__name__)


class DealService:
    """Service for deal business logic."""
    
    def __init__(self, deal_repo: DealRepository):
        self.deal_repo = deal_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal."""
        # Validate business rules
        await self._validate_deal_creation(deal)
        
        # Set active days bitmask
        if not deal.days_mask:
            deal.set_active_days([DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY])
        
        created_deal = await self.deal_repo.create(deal)
        self.logger.info("Deal created", deal_id=str(created_deal.id), venue_id=str(created_deal.venue_id))
        
        return created_deal
    
    async def get_deal(self, deal_id: uuid.UUID) -> Deal:
        """Get deal by ID."""
        deal = await self.deal_repo.get_by_id(deal_id)
        if not deal:
            raise NotFoundError(f"Deal with id {deal_id} not found")
        
        return deal
    
    async def update_deal(self, deal: Deal) -> Deal:
        """Update deal."""
        # Validate business rules
        await self._validate_deal_update(deal)
        
        updated_deal = await self.deal_repo.update(deal)
        self.logger.info("Deal updated", deal_id=str(updated_deal.id))
        
        return updated_deal
    
    async def delete_deal(self, deal_id: uuid.UUID) -> bool:
        """Delete deal."""
        success = await self.deal_repo.delete(deal_id)
        if success:
            self.logger.info("Deal deleted", deal_id=str(deal_id))
        else:
            self.logger.warning("Failed to delete deal", deal_id=str(deal_id))
        
        return success
    
    async def list_venue_deals(self, venue_id: uuid.UUID, active_only: bool = True) -> List[Deal]:
        """List deals by venue."""
        return await self.deal_repo.list_by_venue(venue_id, active_only)
    
    async def list_nearby_deals(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Deal]:
        """List active deals nearby."""
        return await self.deal_repo.list_active_nearby(lat, lng, radius_km, category, limit, offset)
    
    async def list_featured_deals(self, limit: int = 20) -> List[Deal]:
        """List featured deals."""
        return await self.deal_repo.list_featured(limit)
    
    async def feature_deal(self, deal_id: uuid.UUID) -> Deal:
        """Feature a deal."""
        deal = await self.get_deal(deal_id)
        deal.feature()
        updated_deal = await self.deal_repo.update(deal)
        
        self.logger.info("Deal featured", deal_id=str(deal_id))
        return updated_deal
    
    async def unfeature_deal(self, deal_id: uuid.UUID) -> Deal:
        """Unfeature a deal."""
        deal = await self.get_deal(deal_id)
        deal.unfeature()
        updated_deal = await self.deal_repo.update(deal)
        
        self.logger.info("Deal unfeatured", deal_id=str(deal_id))
        return updated_deal
    
    async def verify_deal(self, deal_id: uuid.UUID, verified_by: uuid.UUID) -> Deal:
        """Mark deal as verified."""
        deal = await self.get_deal(deal_id)
        deal.verify(verified_by)
        updated_deal = await self.deal_repo.update(deal)
        
        self.logger.info("Deal verified", deal_id=str(deal_id), verified_by=str(verified_by))
        return updated_deal
    
    async def redeem_deal(self, deal_id: uuid.UUID) -> bool:
        """Redeem a deal."""
        deal = await self.get_deal(deal_id)
        
        if not deal.is_available:
            self.logger.warning("Deal not available for redemption", deal_id=str(deal_id))
            return False
        
        success = deal.redeem()
        if success:
            await self.deal_repo.update(deal)
            self.logger.info("Deal redeemed", deal_id=str(deal_id))
        
        return success
    
    async def _validate_deal_creation(self, deal: Deal) -> None:
        """Validate deal creation business rules."""
        # Validate pricing
        if deal.original_price is not None and deal.deal_price is not None:
            if deal.deal_price >= deal.original_price:
                raise BusinessRuleError(
                    "Deal price must be less than original price",
                    code="INVALID_DEAL_PRICING"
                )
        
        # Validate time range
        if deal.start_time and deal.end_time:
            if deal.start_time >= deal.end_time:
                raise BusinessRuleError(
                    "Start time must be before end time",
                    code="INVALID_TIME_RANGE"
                )
        
        # Validate redemptions
        if deal.max_redemptions is not None and deal.max_redemptions <= 0:
            raise BusinessRuleError(
                "Max redemptions must be positive",
                code="INVALID_MAX_REDEMPTIONS"
            )
    
    async def _validate_deal_update(self, deal: Deal) -> None:
        """Validate deal update business rules."""
        # Check if deal exists
        existing = await self.deal_repo.get_by_id(deal.id)
        if not existing:
            raise NotFoundError(f"Deal with id {deal.id} not found")
        
        # Re-validate creation rules
        await self._validate_deal_creation(deal)
