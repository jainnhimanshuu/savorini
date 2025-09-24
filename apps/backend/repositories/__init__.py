"""Repository layer for data access."""

from .base import BaseRepository
from .deal_repository import DealRepositoryImpl
from .event_log_repository import EventLogRepositoryImpl
from .favorite_repository import FavoriteRepositoryImpl
from .flag_repository import FlagRepositoryImpl
from .interfaces import (
    DealRepository,
    EventLogRepository,
    FavoriteRepository,
    FlagRepository,
    MediaRepository,
    ProvinceRuleRepository,
    UserRepository,
    VenueRepository,
)
from .media_repository import MediaRepositoryImpl
from .models import Base
from .province_rule_repository import ProvinceRuleRepositoryImpl
from .user_repository import UserRepositoryImpl
from .venue_repository import VenueRepositoryImpl

__all__ = [
    # Base
    "BaseRepository",
    "Base",
    
    # Interfaces
    "UserRepository",
    "VenueRepository",
    "DealRepository",
    "MediaRepository",
    "FavoriteRepository",
    "FlagRepository",
    "ProvinceRuleRepository",
    "EventLogRepository",
    
    # Implementations
    "UserRepositoryImpl",
    "VenueRepositoryImpl",
    "DealRepositoryImpl",
    "MediaRepositoryImpl",
    "FavoriteRepositoryImpl",
    "FlagRepositoryImpl",
    "ProvinceRuleRepositoryImpl",
    "EventLogRepositoryImpl",
]
