"""SQLAlchemy models."""

import uuid
from datetime import datetime
from typing import List, Optional

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from domain.enums import (
    DayOfWeek,
    DealCategory,
    EventType,
    FlagReason,
    FlagStatus,
    LicenseType,
    MediaType,
    PriceDisplayMode,
    Province,
    SecondaryHoursType,
    UserRole,
    VenueStatus,
)

Base = declarative_base()


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255))
    provider_sub = Column(String(255), unique=True)  # OAuth provider subject
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    age_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    venues = relationship("Venue", back_populates="vendor")
    favorites = relationship("Favorite", back_populates="user")
    flags = relationship("Flag", back_populates="user")
    event_logs = relationship("EventLog", back_populates="user")


class Venue(Base):
    """Venue model."""
    
    __tablename__ = "venues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    
    # Location
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    province = Column(Enum(Province), nullable=False, index=True)
    postal_code = Column(String(10))
    geo = Column(Geometry("POINT", srid=4326))  # PostGIS point
    
    # Contact
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(500))
    
    # Business details
    license_type = Column(Enum(LicenseType), nullable=False)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(VenueStatus), default=VenueStatus.PENDING, index=True)
    
    # Features
    has_patio = Column(Boolean, default=False)
    has_parking = Column(Boolean, default=False)
    has_wifi = Column(Boolean, default=False)
    is_accessible = Column(Boolean, default=False)
    
    # Metadata
    google_place_id = Column(String(255), unique=True)
    last_verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vendor = relationship("User", back_populates="venues")
    hours = relationship("Hours", back_populates="venue", cascade="all, delete-orphan")
    secondary_hours = relationship("SecondaryHours", back_populates="venue", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="venue", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="venue", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="venue")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint("vendor_id", "name", name="uq_venue_vendor_name"),
    )


class Hours(Base):
    """Regular operating hours model."""
    
    __tablename__ = "hours"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"), nullable=False)
    day = Column(Enum(DayOfWeek), nullable=False)
    open_time = Column(Time)
    close_time = Column(Time)
    is_closed = Column(Boolean, default=False)
    
    # Relationships
    venue = relationship("Venue", back_populates="hours")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("venue_id", "day", name="uq_hours_venue_day"),
    )


class SecondaryHours(Base):
    """Secondary hours (happy hour, late night, etc.) model."""
    
    __tablename__ = "secondary_hours"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"), nullable=False)
    type = Column(Enum(SecondaryHoursType), nullable=False)
    day = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    venue = relationship("Venue", back_populates="secondary_hours")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("venue_id", "type", "day", name="uq_secondary_hours_venue_type_day"),
    )


class Deal(Base):
    """Deal model."""
    
    __tablename__ = "deals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(Enum(DealCategory), nullable=False, index=True)
    
    # Pricing
    original_price = Column(Float)
    deal_price = Column(Float)
    price_display_mode = Column(Enum(PriceDisplayMode), default=PriceDisplayMode.SHOW)
    
    # Timing
    days_mask = Column(Integer, default=0)  # Bitmask for days
    start_time = Column(Time)
    end_time = Column(Time)
    
    # Restrictions
    restrictions = Column(String(500))
    terms = Column(Text)
    min_purchase = Column(Float)
    max_redemptions = Column(Integer)
    redemptions_used = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    requires_age_verification = Column(Boolean, default=False)
    
    # Verification
    last_verified_at = Column(DateTime)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    venue = relationship("Venue", back_populates="deals")
    verifier = relationship("User", foreign_keys=[verified_by])
    
    # Indexes
    __table_args__ = (
        # Composite index for active deals by venue
        # Index("idx_deals_venue_active", "venue_id", "is_active"),
    )


class ProvinceRule(Base):
    """Province-specific regulatory rules model."""
    
    __tablename__ = "province_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    province = Column(Enum(Province), unique=True, nullable=False)
    allow_price_display = Column(Boolean, default=True)
    brand_logo_ok = Column(Boolean, default=True)
    disclaimer = Column(Text)
    
    # Alcohol-specific rules
    require_age_verification = Column(Boolean, default=False)
    min_age = Column(Integer, default=18)
    
    # Display restrictions
    hide_alcohol_brands = Column(Boolean, default=False)
    hide_alcohol_prices = Column(Boolean, default=False)
    require_food_with_alcohol = Column(Boolean, default=False)
    
    # Time restrictions
    alcohol_sales_start_time = Column(String(5))  # "11:00"
    alcohol_sales_end_time = Column(String(5))    # "02:00"
    
    # Marketing restrictions
    allow_happy_hour_marketing = Column(Boolean, default=True)
    max_discount_percentage = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Media(Base):
    """Media model for venue images, menus, etc."""
    
    __tablename__ = "media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"), nullable=False, index=True)
    type = Column(Enum(MediaType), nullable=False)
    uri = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    caption = Column(String(500))
    
    # File metadata
    filename = Column(String(255))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    width = Column(Integer)
    height = Column(Integer)
    
    # Display options
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Upload metadata
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    original_filename = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    venue = relationship("Venue", back_populates="media")
    uploader = relationship("User", foreign_keys=[uploaded_by])


class Favorite(Base):
    """User favorite venues model."""
    
    __tablename__ = "favorites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("venues.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    venue = relationship("Venue", back_populates="favorites")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "venue_id", name="uq_favorite_user_venue"),
    )


class Flag(Base):
    """Flag/report model for content moderation."""
    
    __tablename__ = "flags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_type = Column(String(50), nullable=False)  # "DEAL", "VENUE"
    target_id = Column(UUID(as_uuid=True), nullable=False)
    reason = Column(Enum(FlagReason), nullable=False)
    description = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Enum(FlagStatus), default=FlagStatus.PENDING)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="flags", foreign_keys=[user_id])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    # Indexes
    __table_args__ = (
        # Index("idx_flags_target", "target_type", "target_id"),
        # Index("idx_flags_status", "status"),
    )


class EventLog(Base):
    """Analytics event log model."""
    
    __tablename__ = "event_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Enum(EventType), nullable=False, index=True)
    target_type = Column(String(50))  # "DEAL", "VENUE"
    target_id = Column(UUID(as_uuid=True), index=True)
    session_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    meta = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="event_logs")
    
    # Indexes for analytics queries
    __table_args__ = (
        # Index("idx_events_type_created", "type", "created_at"),
        # Index("idx_events_target_created", "target_type", "target_id", "created_at"),
    )
