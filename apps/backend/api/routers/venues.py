"""Venue routes."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from api.schemas.common import ApiResponse, IdResponse, PaginatedResponse
from core.security import TokenData, get_current_vendor
from domain.entities import Venue, VenueWithDetails
from domain.enums import LicenseType, Province, VenueStatus

router = APIRouter()


class VenueCreateRequest(BaseModel):
    """Venue creation request."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    address: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=100)
    province: Province
    postal_code: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    website: Optional[str] = None
    license_type: LicenseType
    has_patio: bool = False
    has_parking: bool = False
    has_wifi: bool = False
    is_accessible: bool = False


class VenueUpdateRequest(BaseModel):
    """Venue update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    province: Optional[Province] = None
    postal_code: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    website: Optional[str] = None
    license_type: Optional[LicenseType] = None
    has_patio: Optional[bool] = None
    has_parking: Optional[bool] = None
    has_wifi: Optional[bool] = None
    is_accessible: Optional[bool] = None


class VenueResponse(BaseModel):
    """Venue response."""
    id: UUID
    name: str
    slug: Optional[str]
    description: Optional[str]
    address: str
    city: str
    province: str
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    license_type: LicenseType
    status: VenueStatus
    has_patio: bool
    has_parking: bool
    has_wifi: bool
    is_accessible: bool
    distance_km: Optional[float] = None
    deals_count: int = 0
    
    class Config:
        from_attributes = True


@router.get("", response_model=PaginatedResponse[VenueResponse])
async def search_venues(
    query: Optional[str] = Query(None, description="Search query"),
    city: Optional[str] = Query(None, description="City filter"),
    province: Optional[Province] = Query(None, description="Province filter"),
    license_type: Optional[LicenseType] = Query(None, description="License type filter"),
    has_food: bool = Query(False, description="Must serve food"),
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Latitude for distance"),
    lng: Optional[float] = Query(None, ge=-180, le=180, description="Longitude for distance"),
    radius_km: Optional[float] = Query(None, ge=0.1, le=50, description="Search radius"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[VenueResponse]:
    """Search venues with filters."""
    
    # TODO: Implement venue search with:
    # 1. Text search on name, description, address
    # 2. Geographic filtering if lat/lng provided
    # 3. Status filtering (only active venues for public)
    # 4. License type and feature filters
    # 5. Pagination and sorting
    
    # Mock data for now
    mock_venues = [
        VenueResponse(
            id=UUID("12345678-1234-5678-9012-123456789012"),
            name="The Local Pub",
            slug="the-local-pub",
            description="Cozy neighborhood pub with great atmosphere",
            address="123 Main St",
            city="Toronto",
            province="ON",
            postal_code="M5V 1A1",
            phone="416-555-0123",
            email="info@localpub.com",
            website="https://localpub.com",
            license_type=LicenseType.PUB,
            status=VenueStatus.ACTIVE,
            has_patio=True,
            has_parking=False,
            has_wifi=True,
            is_accessible=True,
            distance_km=0.5 if lat and lng else None,
            deals_count=3,
        ),
    ]
    
    # Apply filters to mock data
    filtered_venues = mock_venues
    if city:
        filtered_venues = [v for v in filtered_venues if v.city.lower() == city.lower()]
    if province:
        filtered_venues = [v for v in filtered_venues if v.province == province.value]
    if license_type:
        filtered_venues = [v for v in filtered_venues if v.license_type == license_type]
    
    # Pagination
    total = len(filtered_venues)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = filtered_venues[start_idx:end_idx]
    
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


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(venue_id: UUID) -> VenueResponse:
    """Get venue by ID."""
    
    # TODO: Implement venue lookup by ID
    # Include deals, hours, media, etc.
    
    # Mock response for now
    return VenueResponse(
        id=venue_id,
        name="The Local Pub",
        slug="the-local-pub",
        description="Cozy neighborhood pub with great atmosphere",
        address="123 Main St",
        city="Toronto",
        province="ON",
        postal_code="M5V 1A1",
        phone="416-555-0123",
        email="info@localpub.com",
        website="https://localpub.com",
        license_type=LicenseType.PUB,
        status=VenueStatus.ACTIVE,
        has_patio=True,
        has_parking=False,
        has_wifi=True,
        is_accessible=True,
        deals_count=3,
    )


@router.post("", response_model=IdResponse)
async def create_venue(
    request: VenueCreateRequest,
    current_user: TokenData = Depends(get_current_vendor),
) -> IdResponse:
    """Create new venue (vendor only)."""
    
    # TODO: Implement venue creation
    # 1. Validate vendor permissions
    # 2. Geocode address
    # 3. Create venue in pending status
    # 4. Return venue ID
    
    from uuid import uuid4
    
    venue_id = uuid4()
    
    return IdResponse(id=venue_id)


@router.put("/{venue_id}", response_model=VenueResponse)
async def update_venue(
    venue_id: UUID,
    request: VenueUpdateRequest,
    current_user: TokenData = Depends(get_current_vendor),
) -> VenueResponse:
    """Update venue (vendor only)."""
    
    # TODO: Implement venue update
    # 1. Validate venue ownership
    # 2. Update fields
    # 3. Re-geocode if address changed
    # 4. Return updated venue
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Venue update not implemented yet",
    )


@router.delete("/{venue_id}")
async def delete_venue(
    venue_id: UUID,
    current_user: TokenData = Depends(get_current_vendor),
) -> dict:
    """Delete venue (vendor only)."""
    
    # TODO: Implement venue deletion
    # 1. Validate venue ownership
    # 2. Soft delete venue
    # 3. Deactivate all deals
    
    return {"message": "Venue deleted successfully"}
