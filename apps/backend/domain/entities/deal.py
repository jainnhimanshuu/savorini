"""Deal domain entity."""

import uuid
from datetime import datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field

from ..enums import DayOfWeek, DealCategory, PriceDisplayMode
from .base import BaseEntity


class Deal(BaseEntity):
    """Deal entity."""
    
    venue_id: uuid.UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: DealCategory
    
    # Pricing
    original_price: Optional[float] = Field(None, ge=0)
    deal_price: Optional[float] = Field(None, ge=0)
    price_display_mode: PriceDisplayMode = PriceDisplayMode.SHOW
    
    # Timing
    days_mask: int = 0  # Bitmask for days (1=Monday, 2=Tuesday, etc.)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    # Restrictions and details
    restrictions: Optional[str] = Field(None, max_length=500)
    terms: Optional[str] = Field(None, max_length=1000)
    min_purchase: Optional[float] = Field(None, ge=0)
    max_redemptions: Optional[int] = Field(None, ge=1)
    redemptions_used: int = Field(default=0, ge=0)
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    requires_age_verification: bool = False
    
    # Verification
    last_verified_at: Optional[datetime] = None
    verified_by: Optional[uuid.UUID] = None
    
    @property
    def active_days(self) -> List[DayOfWeek]:
        """Get list of active days."""
        days = []
        day_mapping = [
            DayOfWeek.MONDAY,
            DayOfWeek.TUESDAY,
            DayOfWeek.WEDNESDAY,
            DayOfWeek.THURSDAY,
            DayOfWeek.FRIDAY,
            DayOfWeek.SATURDAY,
            DayOfWeek.SUNDAY,
        ]
        
        for i, day in enumerate(day_mapping):
            if self.days_mask & (1 << i):
                days.append(day)
        
        return days
    
    def set_active_days(self, days: List[DayOfWeek]) -> None:
        """Set active days using bitmask."""
        day_mapping = {
            DayOfWeek.MONDAY: 0,
            DayOfWeek.TUESDAY: 1,
            DayOfWeek.WEDNESDAY: 2,
            DayOfWeek.THURSDAY: 3,
            DayOfWeek.FRIDAY: 4,
            DayOfWeek.SATURDAY: 5,
            DayOfWeek.SUNDAY: 6,
        }
        
        self.days_mask = 0
        for day in days:
            if day in day_mapping:
                self.days_mask |= (1 << day_mapping[day])
        
        self.updated_at = datetime.utcnow()
    
    @property
    def savings_amount(self) -> Optional[float]:
        """Calculate savings amount."""
        if self.original_price and self.deal_price:
            return self.original_price - self.deal_price
        return None
    
    @property
    def savings_percentage(self) -> Optional[float]:
        """Calculate savings percentage."""
        if self.original_price and self.deal_price and self.original_price > 0:
            return ((self.original_price - self.deal_price) / self.original_price) * 100
        return None
    
    @property
    def is_available(self) -> bool:
        """Check if deal is currently available."""
        if not self.is_active:
            return False
        
        if self.max_redemptions and self.redemptions_used >= self.max_redemptions:
            return False
        
        return True
    
    def redeem(self) -> bool:
        """Redeem the deal."""
        if not self.is_available:
            return False
        
        if self.max_redemptions and self.redemptions_used >= self.max_redemptions:
            return False
        
        self.redemptions_used += 1
        self.updated_at = datetime.utcnow()
        return True
    
    def verify(self, verified_by: uuid.UUID) -> None:
        """Mark deal as verified."""
        self.last_verified_at = datetime.utcnow()
        self.verified_by = verified_by
        self.updated_at = datetime.utcnow()
    
    def feature(self) -> None:
        """Mark deal as featured."""
        self.is_featured = True
        self.updated_at = datetime.utcnow()
    
    def unfeature(self) -> None:
        """Unmark deal as featured."""
        self.is_featured = False
        self.updated_at = datetime.utcnow()


class DealWithVenue(BaseModel):
    """Deal with venue information."""
    
    deal: Deal
    venue_name: str
    venue_address: str
    venue_city: str
    venue_province: str
    distance_km: Optional[float] = None
    
    class Config:
        from_attributes = True
