"""Favorite domain entity."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from .base import TimestampedEntity


class Favorite(TimestampedEntity):
    """User favorite venue."""
    
    user_id: uuid.UUID
    venue_id: uuid.UUID
    
    class Config:
        from_attributes = True


class FavoriteWithVenue(BaseModel):
    """Favorite with venue information."""
    
    favorite: Favorite
    venue_id: uuid.UUID
    venue_name: str
    venue_address: str
    venue_city: str
    venue_province: str
    distance_km: float | None = None
    
    class Config:
        from_attributes = True
