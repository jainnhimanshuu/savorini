"""Domain entities."""

from .analytics import AnalyticsSummary, EventBatch, EventLog
from .base import BaseEntity, TimestampedEntity
from .deal import Deal, DealWithVenue
from .favorite import Favorite, FavoriteWithVenue
from .flag import Flag, FlagWithDetails
from .media import Media, MediaUploadRequest, MediaUploadResponse
from .province_rule import ProvinceRule, DEFAULT_PROVINCE_RULES
from .user import User, UserProfile
from .venue import Hours, SecondaryHours, Venue, VenueWithDetails

__all__ = [
    # Base
    "BaseEntity",
    "TimestampedEntity",
    # User
    "User",
    "UserProfile", 
    # Venue
    "Venue",
    "Hours",
    "SecondaryHours",
    "VenueWithDetails",
    # Deal
    "Deal",
    "DealWithVenue",
    # Media
    "Media",
    "MediaUploadRequest",
    "MediaUploadResponse",
    # Province Rules
    "ProvinceRule",
    "DEFAULT_PROVINCE_RULES",
    # Favorites
    "Favorite",
    "FavoriteWithVenue",
    # Flags/Reports
    "Flag",
    "FlagWithDetails",
    # Analytics
    "EventLog",
    "EventBatch",
    "AnalyticsSummary",
]
