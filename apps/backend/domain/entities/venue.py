"""Venue domain entity."""

import uuid
from datetime import datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
from shapely.geometry import Point

from ..enums import DayOfWeek, LicenseType, SecondaryHoursType, VenueStatus
from .base import BaseEntity


class Venue(BaseEntity):
    """Venue entity."""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = None
    description: Optional[str] = None
    
    # Location
    address: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=100)
    province: str = Field(..., min_length=2, max_length=2)
    postal_code: Optional[str] = Field(None, max_length=10)
    geo: Optional[Point] = None  # PostGIS POINT
    
    # Contact
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Business details
    license_type: LicenseType
    vendor_id: uuid.UUID
    status: VenueStatus = VenueStatus.PENDING
    
    # Features
    has_patio: bool = False
    has_parking: bool = False
    has_wifi: bool = False
    is_accessible: bool = False
    
    # Metadata
    google_place_id: Optional[str] = None
    last_verified_at: Optional[datetime] = None
    
    def activate(self) -> None:
        """Activate venue."""
        self.status = VenueStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def suspend(self) -> None:
        """Suspend venue."""
        self.status = VenueStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def verify(self) -> None:
        """Mark venue as verified."""
        self.last_verified_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class Hours(BaseModel):
    """Regular operating hours."""
    
    venue_id: uuid.UUID
    day: DayOfWeek
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    is_closed: bool = False
    
    class Config:
        from_attributes = True
    
    @property
    def is_24_hours(self) -> bool:
        """Check if venue is open 24 hours."""
        return (
            not self.is_closed 
            and self.open_time == time(0, 0) 
            and self.close_time == time(23, 59)
        )


class SecondaryHours(BaseModel):
    """Secondary hours (happy hour, late night, etc.)."""
    
    venue_id: uuid.UUID
    type: SecondaryHoursType
    day: DayOfWeek
    start_time: time
    end_time: time
    is_active: bool = True
    
    class Config:
        from_attributes = True


class VenueWithDetails(BaseModel):
    """Venue with associated data."""
    
    venue: Venue
    hours: List[Hours]
    secondary_hours: List[SecondaryHours]
    deals_count: int = 0
    distance_km: Optional[float] = None
    
    class Config:
        from_attributes = True
