"""Flag/Report domain entity."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..enums import FlagReason, FlagStatus
from .base import BaseEntity


class Flag(BaseEntity):
    """Flag/Report entity for reporting issues."""
    
    target_type: str = Field(..., min_length=1, max_length=50)  # "DEAL" or "VENUE"
    target_id: uuid.UUID
    reason: FlagReason
    description: Optional[str] = Field(None, max_length=1000)
    user_id: uuid.UUID
    status: FlagStatus = FlagStatus.PENDING
    
    # Resolution
    resolved_by: Optional[uuid.UUID] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = Field(None, max_length=1000)
    
    def resolve(self, resolved_by: uuid.UUID, notes: Optional[str] = None) -> None:
        """Resolve the flag."""
        self.status = FlagStatus.RESOLVED
        self.resolved_by = resolved_by
        self.resolved_at = datetime.utcnow()
        self.resolution_notes = notes
        self.updated_at = datetime.utcnow()
    
    def dismiss(self, resolved_by: uuid.UUID, notes: Optional[str] = None) -> None:
        """Dismiss the flag."""
        self.status = FlagStatus.DISMISSED
        self.resolved_by = resolved_by
        self.resolved_at = datetime.utcnow()
        self.resolution_notes = notes
        self.updated_at = datetime.utcnow()


class FlagWithDetails(BaseModel):
    """Flag with additional details."""
    
    flag: Flag
    target_name: str  # Venue name or deal title
    reporter_email: str
    resolved_by_name: Optional[str] = None
    
    class Config:
        from_attributes = True
