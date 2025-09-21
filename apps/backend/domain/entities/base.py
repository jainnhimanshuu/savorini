"""Base entity classes."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base entity with common fields."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: str,
        }


class TimestampedEntity(BaseModel):
    """Entity with timestamp fields only."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
