"""Province rule domain entity."""

from typing import Optional

from pydantic import BaseModel, Field

from ..enums import Province
from .base import TimestampedEntity


class ProvinceRule(TimestampedEntity):
    """Province-specific regulatory rules."""
    
    province: Province
    allow_price_display: bool = True
    brand_logo_ok: bool = True
    disclaimer: Optional[str] = Field(None, max_length=1000)
    
    # Alcohol-specific rules
    require_age_verification: bool = False
    min_age: int = 18
    
    # Display restrictions
    hide_alcohol_brands: bool = False
    hide_alcohol_prices: bool = False
    require_food_with_alcohol: bool = False
    
    # Time restrictions
    alcohol_sales_start_time: Optional[str] = None  # "11:00"
    alcohol_sales_end_time: Optional[str] = None    # "02:00"
    
    # Marketing restrictions
    allow_happy_hour_marketing: bool = True
    max_discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    
    class Config:
        from_attributes = True


# Default province rules
DEFAULT_PROVINCE_RULES = {
    Province.ON: ProvinceRule(
        province=Province.ON,
        allow_price_display=True,
        brand_logo_ok=True,
        require_age_verification=True,
        min_age=19,
        alcohol_sales_start_time="11:00",
        alcohol_sales_end_time="02:00",
        disclaimer="Must be 19+ to consume alcohol. Please drink responsibly.",
    ),
    Province.BC: ProvinceRule(
        province=Province.BC,
        allow_price_display=True,
        brand_logo_ok=True,
        require_age_verification=True,
        min_age=19,
        alcohol_sales_start_time="11:00",
        alcohol_sales_end_time="02:00",
        disclaimer="Must be 19+ to consume alcohol. Please drink responsibly.",
    ),
    Province.AB: ProvinceRule(
        province=Province.AB,
        allow_price_display=False,  # Alberta has stricter rules
        brand_logo_ok=True,
        require_age_verification=True,
        min_age=18,
        alcohol_sales_start_time="11:00",
        alcohol_sales_end_time="02:00",
        disclaimer="Must be 18+ to consume alcohol. Prices subject to change. Please drink responsibly.",
    ),
}
