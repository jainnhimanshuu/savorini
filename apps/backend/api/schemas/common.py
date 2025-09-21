"""Common API schemas."""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    
    data: T
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    page: int = Field(..., ge=1)
    per_page: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)
    pages: int = Field(..., ge=0)
    has_next: bool
    has_prev: bool
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response."""
    
    data: List[T]
    pagination: PaginationMeta
    message: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail."""
    
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: ErrorDetail


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    version: str
    timestamp: str
    services: Optional[Dict[str, str]] = None


class IdResponse(BaseModel):
    """Response with just an ID."""
    
    id: UUID


class MessageResponse(BaseModel):
    """Response with just a message."""
    
    message: str


class BulkOperationResponse(BaseModel):
    """Bulk operation response."""
    
    processed: int
    successful: int
    failed: int
    errors: Optional[List[ErrorDetail]] = None
