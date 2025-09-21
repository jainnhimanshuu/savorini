#!/usr/bin/env python3
"""Seed script for loading sample data into the database."""

import asyncio
import uuid
from datetime import datetime, time
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import init_database, async_session_factory
from domain.enums import (
    DayOfWeek, DealCategory, LicenseType, Province, 
    SecondaryHoursType, UserRole, VenueStatus
)
from repositories.models import User, Venue, Hours, SecondaryHours, Deal, ProvinceRule


# Sample data
SAMPLE_USERS = [
    {
        "email": "admin@happyhour.ca",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXxPQz.1234567890",  # password123
        "role": UserRole.ADMIN,
        "first_name": "Admin",
        "last_name": "User",
        "age_verified": True,
    },
    {
        "email": "vendor@localpub.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXxPQz.1234567890",  # password123
        "role": UserRole.VENDOR,
        "first_name": "John",
        "last_name": "Smith",
        "age_verified": True,
    },
    {
        "email": "user@example.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewXxPQz.1234567890",  # password123
        "role": UserRole.USER,
        "first_name": "Jane",
        "last_name": "Doe",
        "age_verified": True,
    },
]

SAMPLE_VENUES = [
    # Toronto venues
    {
        "name": "The Local Pub",
        "slug": "the-local-pub",
        "description": "Cozy neighborhood pub with great atmosphere and local craft beer",
        "address": "123 Queen St W",
        "city": "Toronto",
        "province": Province.ON,
        "postal_code": "M5H 2M9",
        "phone": "416-555-0123",
        "email": "info@localpub.com",
        "website": "https://localpub.com",
        "license_type": LicenseType.PUB,
        "status": VenueStatus.ACTIVE,
        "has_patio": True,
        "has_parking": False,
        "has_wifi": True,
        "is_accessible": True,
        "lat": 43.6532,
        "lng": -79.3832,
    },
    {
        "name": "Rooftop Lounge",
        "slug": "rooftop-lounge",
        "description": "Upscale rooftop bar with city views and craft cocktails",
        "address": "456 King St W",
        "city": "Toronto", 
        "province": Province.ON,
        "postal_code": "M5V 1M3",
        "phone": "416-555-0456",
        "license_type": LicenseType.LOUNGE,
        "status": VenueStatus.ACTIVE,
        "has_patio": True,
        "has_parking": True,
        "has_wifi": True,
        "is_accessible": False,
        "lat": 43.6426,
        "lng": -79.3871,
    },
    # Vancouver venues
    {
        "name": "Pacific Brewery",
        "slug": "pacific-brewery",
        "description": "Craft brewery with house-made beer and pub food",
        "address": "789 Granville St",
        "city": "Vancouver",
        "province": Province.BC,
        "postal_code": "V6Z 1K3",
        "phone": "604-555-0789",
        "license_type": LicenseType.BREWERY,
        "status": VenueStatus.ACTIVE,
        "has_patio": True,
        "has_parking": False,
        "has_wifi": True,
        "is_accessible": True,
        "lat": 49.2827,
        "lng": -123.1207,
    },
    # Calgary venues
    {
        "name": "Stampede Saloon",
        "slug": "stampede-saloon", 
        "description": "Western-themed bar with live music and dancing",
        "address": "321 17 Ave SW",
        "city": "Calgary",
        "province": Province.AB,
        "postal_code": "T2S 0A1",
        "phone": "403-555-0321",
        "license_type": LicenseType.BAR,
        "status": VenueStatus.ACTIVE,
        "has_patio": False,
        "has_parking": True,
        "has_wifi": True,
        "is_accessible": True,
        "lat": 51.0447,
        "lng": -114.0719,
    },
]

SAMPLE_DEALS = [
    {
        "title": "$5 Wings & $4 Beer",
        "description": "Crispy wings with your choice of sauce, plus domestic beer",
        "category": DealCategory.FOOD,
        "original_price": 13.00,
        "deal_price": 9.00,
        "days_mask": 0b0111000,  # Mon, Tue, Wed
        "start_time": time(15, 0),
        "end_time": time(18, 0),
        "restrictions": "Dine-in only",
        "is_active": True,
        "is_featured": True,
        "requires_age_verification": False,
    },
    {
        "title": "Half Price Cocktails",
        "description": "All premium cocktails 50% off during happy hour",
        "category": DealCategory.DRINK,
        "original_price": 14.00,
        "deal_price": 7.00,
        "days_mask": 0b1111100,  # Mon-Fri
        "start_time": time(17, 0),
        "end_time": time(19, 0),
        "restrictions": "Bar seating only",
        "is_active": True,
        "is_featured": False,
        "requires_age_verification": True,
    },
    {
        "title": "2-for-1 Appetizers",
        "description": "Buy one appetizer, get one free",
        "category": DealCategory.FOOD,
        "original_price": 12.00,
        "deal_price": 12.00,
        "days_mask": 0b0001110,  # Wed, Thu, Fri
        "start_time": time(16, 0),
        "end_time": time(18, 30),
        "is_active": True,
        "is_featured": False,
        "requires_age_verification": False,
    },
]


async def create_users(session: AsyncSession) -> List[User]:
    """Create sample users."""
    users = []
    for user_data in SAMPLE_USERS:
        user = User(**user_data)
        session.add(user)
        users.append(user)
    
    await session.commit()
    print(f"Created {len(users)} users")
    return users


async def create_venues(session: AsyncSession, vendor: User) -> List[Venue]:
    """Create sample venues."""
    venues = []
    for venue_data in SAMPLE_VENUES:
        # Extract lat/lng for PostGIS
        lat = venue_data.pop("lat")
        lng = venue_data.pop("lng")
        
        venue = Venue(
            **venue_data,
            vendor_id=vendor.id,
            # geo=f"POINT({lng} {lat})"  # PostGIS format
        )
        session.add(venue)
        venues.append(venue)
    
    await session.commit()
    print(f"Created {len(venues)} venues")
    return venues


async def create_hours(session: AsyncSession, venues: List[Venue]) -> None:
    """Create operating hours for venues."""
    hours_count = 0
    
    for venue in venues:
        # Regular hours (Mon-Thu: 11am-12am, Fri-Sat: 11am-2am, Sun: 12pm-11pm)
        regular_hours = [
            (DayOfWeek.MONDAY, time(11, 0), time(0, 0)),
            (DayOfWeek.TUESDAY, time(11, 0), time(0, 0)),
            (DayOfWeek.WEDNESDAY, time(11, 0), time(0, 0)),
            (DayOfWeek.THURSDAY, time(11, 0), time(0, 0)),
            (DayOfWeek.FRIDAY, time(11, 0), time(2, 0)),
            (DayOfWeek.SATURDAY, time(11, 0), time(2, 0)),
            (DayOfWeek.SUNDAY, time(12, 0), time(23, 0)),
        ]
        
        for day, open_time, close_time in regular_hours:
            hours = Hours(
                venue_id=venue.id,
                day=day,
                open_time=open_time,
                close_time=close_time,
            )
            session.add(hours)
            hours_count += 1
        
        # Happy hour (Mon-Fri: 3pm-6pm)
        for day in [DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY]:
            happy_hour = SecondaryHours(
                venue_id=venue.id,
                type=SecondaryHoursType.HAPPY_HOUR,
                day=day,
                start_time=time(15, 0),
                end_time=time(18, 0),
            )
            session.add(happy_hour)
            hours_count += 1
    
    await session.commit()
    print(f"Created {hours_count} hours entries")


async def create_deals(session: AsyncSession, venues: List[Venue]) -> None:
    """Create sample deals."""
    deals_count = 0
    
    for venue in venues[:3]:  # First 3 venues get deals
        for i, deal_data in enumerate(SAMPLE_DEALS):
            if i >= 2 and venue.province == Province.AB:
                # Alberta gets fewer deals due to restrictions
                break
                
            deal = Deal(
                **deal_data,
                venue_id=venue.id,
            )
            session.add(deal)
            deals_count += 1
    
    await session.commit()
    print(f"Created {deals_count} deals")


async def create_province_rules(session: AsyncSession) -> None:
    """Create province-specific rules."""
    rules = [
        ProvinceRule(
            province=Province.ON,
            allow_price_display=True,
            brand_logo_ok=True,
            require_age_verification=True,
            min_age=19,
            disclaimer="Must be 19+ to consume alcohol. Please drink responsibly.",
        ),
        ProvinceRule(
            province=Province.BC,
            allow_price_display=True,
            brand_logo_ok=True,
            require_age_verification=True,
            min_age=19,
            disclaimer="Must be 19+ to consume alcohol. Please drink responsibly.",
        ),
        ProvinceRule(
            province=Province.AB,
            allow_price_display=False,  # Alberta restricts price display
            brand_logo_ok=True,
            require_age_verification=True,
            min_age=18,
            disclaimer="Must be 18+ to consume alcohol. Prices subject to change. Please drink responsibly.",
        ),
    ]
    
    for rule in rules:
        session.add(rule)
    
    await session.commit()
    print(f"Created {len(rules)} province rules")


async def main():
    """Main seeding function."""
    print("🌱 Starting database seeding...")
    
    # Initialize database
    await init_database()
    
    async with async_session_factory() as session:
        # Create users
        users = await create_users(session)
        vendor = next(u for u in users if u.role == UserRole.VENDOR)
        
        # Create venues
        venues = await create_venues(session, vendor)
        
        # Create hours
        await create_hours(session, venues)
        
        # Create deals
        await create_deals(session, venues)
        
        # Create province rules
        await create_province_rules(session)
    
    print("✅ Database seeding completed!")
    print("\n📊 Sample data created:")
    print(f"  👥 Users: {len(SAMPLE_USERS)}")
    print(f"  🏢 Venues: {len(SAMPLE_VENUES)}")
    print(f"  🍻 Deals: Multiple per venue")
    print(f"  📍 Provinces: ON, BC, AB")
    print("\n🔐 Test accounts:")
    print("  Admin: admin@happyhour.ca / password123")
    print("  Vendor: vendor@localpub.com / password123") 
    print("  User: user@example.com / password123")


if __name__ == "__main__":
    asyncio.run(main())
