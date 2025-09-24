"""Feed routes for discovering deals."""

from datetime import datetime, time
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.schemas.common import PaginatedResponse
from core.logging import get_logger
from domain.entities import DealWithVenue
from domain.enums import DealCategory, Province

router = APIRouter()
logger = get_logger(__name__)


class FeedFilters(BaseModel):
    """Feed filters."""
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=10, ge=0.1, le=50)
    when: str = Field(default="now", pattern="^(now|soon|today|tonight)$")
    category: Optional[DealCategory] = None
    province: Optional[Province] = None
    has_food_only: bool = False
    min_savings: Optional[float] = Field(None, ge=0)


class FeedItem(BaseModel):
    """Feed item response."""
    deal_id: str
    venue_id: str
    title: str
    description: Optional[str]
    category: DealCategory
    venue_name: str
    venue_address: str
    distance_km: float
    starts_at: Optional[time]
    ends_at: Optional[time]
    savings_amount: Optional[float]
    savings_percentage: Optional[float]
    is_featured: bool
    image_url: Optional[str] = None


class FeedResponse(PaginatedResponse[FeedItem]):
    """Feed response with metadata."""
    when: str
    location: dict
    filters_applied: dict


@router.get("", response_model=FeedResponse)
async def get_feed(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius_km: float = Query(default=10, ge=0.1, le=50, description="Search radius in km"),
    when: str = Query(default="now", pattern="^(now|soon|today|tonight)$", description="Time filter"),
    category: Optional[DealCategory] = Query(None, description="Deal category filter"),
    province: Optional[Province] = Query(None, description="Province filter"),
    has_food_only: bool = Query(False, description="Only venues with food"),
    min_savings: Optional[float] = Query(None, ge=0, description="Minimum savings amount"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> FeedResponse:
    """Get personalized feed of deals based on location and preferences."""
    
    logger.info(
        "Feed request",
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        when=when,
        category=category,
        province=province,
    )
    
    # TODO: Implement actual feed logic with:
    # 1. Geo search for venues within radius
    # 2. Filter by active deals based on time window
    # 3. Apply category/province filters
    # 4. Sort by distance, featured status, popularity
    # 5. Apply pagination
    # 6. Cache results in Redis
    
    # Mock feed data for now
    mock_items = [
        FeedItem(
            deal_id="deal-1",
            venue_id="venue-1",
            title="$5 Wings & $4 Beer",
            description="Crispy wings with your choice of sauce",
            category=DealCategory.FOOD,
            venue_name="The Local Pub",
            venue_address="123 Main St",
            distance_km=0.5,
            starts_at=time(15, 0),  # 3 PM
            ends_at=time(18, 0),    # 6 PM
            savings_amount=8.0,
            savings_percentage=40.0,
            is_featured=True,
            image_url="https://example.com/wings.jpg",
        ),
        FeedItem(
            deal_id="deal-2",
            venue_id="venue-2",
            title="Half Price Cocktails",
            description="All premium cocktails 50% off",
            category=DealCategory.DRINK,
            venue_name="Rooftop Lounge",
            venue_address="456 Queen St",
            distance_km=1.2,
            starts_at=time(17, 0),  # 5 PM
            ends_at=time(19, 0),    # 7 PM
            savings_amount=12.0,
            savings_percentage=50.0,
            is_featured=False,
            image_url="https://example.com/cocktails.jpg",
        ),
    ]
    
    # Filter mock data based on request
    filtered_items = mock_items
    if category:
        filtered_items = [item for item in filtered_items if item.category == category]
    
    # Calculate pagination
    total = len(filtered_items)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = filtered_items[start_idx:end_idx]
    
    from api.schemas.common import PaginationMeta
    
    pagination = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        pages=(total + per_page - 1) // per_page,
        has_next=end_idx < total,
        has_prev=page > 1,
    )
    
    return FeedResponse(
        data=page_items,
        pagination=pagination,
        when=when,
        location={"lat": lat, "lng": lng, "radius_km": radius_km},
        filters_applied={
            "category": category.value if category else None,
            "province": province.value if province else None,
            "has_food_only": has_food_only,
            "min_savings": min_savings,
        },
    )


@router.get("/spotlight")
async def get_spotlight_deals(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    limit: int = Query(default=5, ge=1, le=10),
) -> List[FeedItem]:
    """Get spotlight/featured deals for homepage."""
    
    # TODO: Implement spotlight logic
    # - Featured deals only
    # - High-quality venues
    # - Good photography
    # - Verified recently
    
    # Return mock data for now
    return [
        FeedItem(
            deal_id="spotlight-1",
            venue_id="venue-1",
            title="Signature Cocktail Night",
            description="Try our award-winning cocktails",
            category=DealCategory.DRINK,
            venue_name="The Distillery",
            venue_address="789 King St",
            distance_km=2.1,
            starts_at=time(18, 0),
            ends_at=time(22, 0),
            savings_amount=15.0,
            savings_percentage=30.0,
            is_featured=True,
            image_url="https://example.com/cocktail-night.jpg",
        )
    ]
