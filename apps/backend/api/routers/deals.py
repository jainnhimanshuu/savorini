"""Deal routes."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from api.schemas.common import ApiResponse, IdResponse, PaginatedResponse
from core.security import TokenData, get_current_vendor
from domain.entities import Deal
from domain.enums import DayOfWeek, DealCategory, PriceDisplayMode

router = APIRouter()


class DealCreateRequest(BaseModel):
    """Deal creation request."""
    venue_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: DealCategory
    original_price: Optional[float] = Field(None, ge=0)
    deal_price: Optional[float] = Field(None, ge=0)
    active_days: List[DayOfWeek] = Field(..., min_items=1)
    start_time: Optional[str] = Field(None, regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    end_time: Optional[str] = Field(None, regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    restrictions: Optional[str] = Field(None, max_length=500)
    terms: Optional[str] = Field(None, max_length=1000)
    min_purchase: Optional[float] = Field(None, ge=0)
    max_redemptions: Optional[int] = Field(None, ge=1)
    requires_age_verification: bool = False


class DealUpdateRequest(BaseModel):
    """Deal update request."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[DealCategory] = None
    original_price: Optional[float] = Field(None, ge=0)
    deal_price: Optional[float] = Field(None, ge=0)
    active_days: Optional[List[DayOfWeek]] = Field(None, min_items=1)
    start_time: Optional[str] = Field(None, regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    end_time: Optional[str] = Field(None, regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    restrictions: Optional[str] = Field(None, max_length=500)
    terms: Optional[str] = Field(None, max_length=1000)
    min_purchase: Optional[float] = Field(None, ge=0)
    max_redemptions: Optional[int] = Field(None, ge=1)
    requires_age_verification: Optional[bool] = None
    is_active: Optional[bool] = None


class DealResponse(BaseModel):
    """Deal response."""
    id: UUID
    venue_id: UUID
    title: str
    description: Optional[str]
    category: DealCategory
    original_price: Optional[float]
    deal_price: Optional[float]
    price_display_mode: PriceDisplayMode
    active_days: List[DayOfWeek]
    start_time: Optional[str]
    end_time: Optional[str]
    restrictions: Optional[str]
    terms: Optional[str]
    savings_amount: Optional[float]
    savings_percentage: Optional[float]
    is_active: bool
    is_featured: bool
    requires_age_verification: bool
    redemptions_used: int
    max_redemptions: Optional[int]
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[DealResponse])
async def search_deals(
    venue_id: Optional[UUID] = Query(None, description="Filter by venue"),
    category: Optional[DealCategory] = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Only active deals"),
    featured_only: bool = Query(False, description="Only featured deals"),
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Latitude"),
    lng: Optional[float] = Query(None, ge=-180, le=180, description="Longitude"),
    radius_km: Optional[float] = Query(None, ge=0.1, le=50, description="Search radius"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[DealResponse]:
    """Search deals with filters."""
    
    # TODO: Implement deal search with:
    # 1. Venue filtering
    # 2. Category filtering
    # 3. Geographic filtering
    # 4. Active/featured filtering
    # 5. Province compliance (price display)
    # 6. Pagination and sorting
    
    # Mock data for now
    mock_deals = [
        DealResponse(
            id=UUID("12345678-1234-5678-9012-123456789012"),
            venue_id=UUID("87654321-4321-8765-2109-876543210987"),
            title="$5 Wings & $4 Beer",
            description="Crispy wings with your choice of sauce",
            category=DealCategory.FOOD,
            original_price=13.0,
            deal_price=9.0,
            price_display_mode=PriceDisplayMode.SHOW,
            active_days=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY],
            start_time="15:00",
            end_time="18:00",
            restrictions="Dine-in only",
            terms="Cannot be combined with other offers",
            savings_amount=4.0,
            savings_percentage=30.8,
            is_active=True,
            is_featured=True,
            requires_age_verification=False,
            redemptions_used=45,
            max_redemptions=100,
            venue_name="The Local Pub",
            venue_address="123 Main St",
        ),
    ]
    
    # Apply filters
    filtered_deals = mock_deals
    if venue_id:
        filtered_deals = [d for d in filtered_deals if d.venue_id == venue_id]
    if category:
        filtered_deals = [d for d in filtered_deals if d.category == category]
    if active_only:
        filtered_deals = [d for d in filtered_deals if d.is_active]
    if featured_only:
        filtered_deals = [d for d in filtered_deals if d.is_featured]
    
    # Pagination
    total = len(filtered_deals)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = filtered_deals[start_idx:end_idx]
    
    from api.schemas.common import PaginationMeta
    
    pagination = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        pages=(total + per_page - 1) // per_page,
        has_next=end_idx < total,
        has_prev=page > 1,
    )
    
    return PaginatedResponse(data=page_items, pagination=pagination)


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: UUID) -> DealResponse:
    """Get deal by ID."""
    
    # TODO: Implement deal lookup by ID
    # Apply province compliance rules
    
    # Mock response
    return DealResponse(
        id=deal_id,
        venue_id=UUID("87654321-4321-8765-2109-876543210987"),
        title="$5 Wings & $4 Beer",
        description="Crispy wings with your choice of sauce",
        category=DealCategory.FOOD,
        original_price=13.0,
        deal_price=9.0,
        price_display_mode=PriceDisplayMode.SHOW,
        active_days=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY],
        start_time="15:00",
        end_time="18:00",
        restrictions="Dine-in only",
        terms="Cannot be combined with other offers",
        savings_amount=4.0,
        savings_percentage=30.8,
        is_active=True,
        is_featured=True,
        requires_age_verification=False,
        redemptions_used=45,
        max_redemptions=100,
        venue_name="The Local Pub",
        venue_address="123 Main St",
    )


@router.post("", response_model=IdResponse)
async def create_deal(
    request: DealCreateRequest,
    current_user: TokenData = Depends(get_current_vendor),
) -> IdResponse:
    """Create new deal (vendor only)."""
    
    # TODO: Implement deal creation
    # 1. Validate venue ownership
    # 2. Create deal in pending status
    # 3. Queue for moderation if needed
    # 4. Return deal ID
    
    from uuid import uuid4
    
    deal_id = uuid4()
    
    return IdResponse(id=deal_id)


@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: UUID,
    request: DealUpdateRequest,
    current_user: TokenData = Depends(get_current_vendor),
) -> DealResponse:
    """Update deal (vendor only)."""
    
    # TODO: Implement deal update
    # 1. Validate deal ownership
    # 2. Update fields
    # 3. Re-queue for moderation if needed
    # 4. Return updated deal
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Deal update not implemented yet",
    )


@router.delete("/{deal_id}")
async def delete_deal(
    deal_id: UUID,
    current_user: TokenData = Depends(get_current_vendor),
) -> dict:
    """Delete deal (vendor only)."""
    
    # TODO: Implement deal deletion
    # 1. Validate deal ownership
    # 2. Soft delete deal
    
    return {"message": "Deal deleted successfully"}


@router.post("/{deal_id}/submit")
async def submit_deal_for_review(
    deal_id: UUID,
    current_user: TokenData = Depends(get_current_vendor),
) -> dict:
    """Submit deal for moderation review."""
    
    # TODO: Implement deal submission
    # 1. Validate deal ownership
    # 2. Add to moderation queue
    # 3. Send notification
    
    return {"message": "Deal submitted for review"}
