"""Media domain entity."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from ..enums import MediaType
from .base import BaseEntity


class Media(BaseEntity):
    """Media entity for venue images, menus, etc."""
    
    venue_id: uuid.UUID
    type: MediaType
    uri: HttpUrl
    alt_text: Optional[str] = Field(None, max_length=255)
    caption: Optional[str] = Field(None, max_length=500)
    
    # File metadata
    filename: Optional[str] = Field(None, max_length=255)
    file_size: Optional[int] = Field(None, ge=0)
    mime_type: Optional[str] = Field(None, max_length=100)
    width: Optional[int] = Field(None, ge=1)
    height: Optional[int] = Field(None, ge=1)
    
    # Display options
    is_primary: bool = False
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True
    
    # Upload metadata
    uploaded_by: uuid.UUID
    original_filename: Optional[str] = Field(None, max_length=255)
    
    def mark_as_primary(self) -> None:
        """Mark this media as primary."""
        self.is_primary = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate this media."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    @property
    def aspect_ratio(self) -> Optional[float]:
        """Calculate aspect ratio."""
        if self.width and self.height and self.height > 0:
            return self.width / self.height
        return None


class MediaUploadRequest(BaseModel):
    """Media upload request."""
    
    venue_id: uuid.UUID
    type: MediaType
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=100)
    file_size: int = Field(..., ge=1, le=10 * 1024 * 1024)  # 10MB max
    alt_text: Optional[str] = Field(None, max_length=255)
    caption: Optional[str] = Field(None, max_length=500)


class MediaUploadResponse(BaseModel):
    """Media upload response."""
    
    upload_url: HttpUrl
    media_id: uuid.UUID
    expires_at: datetime
    
    class Config:
        from_attributes = True
