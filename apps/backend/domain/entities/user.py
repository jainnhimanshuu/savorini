"""User domain entity."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from ..enums import UserRole
from .base import BaseEntity


class User(BaseEntity):
    """User entity."""
    
    email: EmailStr
    hashed_password: Optional[str] = None
    provider_sub: Optional[str] = None  # For OAuth providers
    role: UserRole = UserRole.USER
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    age_verified: bool = False
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or ""
    
    def verify_age(self) -> None:
        """Mark user as age verified."""
        self.age_verified = True
        self.updated_at = datetime.utcnow()
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class UserProfile(BaseModel):
    """User profile data transfer object."""
    
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    age_verified: bool
    is_active: bool
    full_name: str
    created_at: datetime
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True
