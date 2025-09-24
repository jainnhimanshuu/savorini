"""User service for user management."""

import uuid
from typing import List, Optional

from domain.entities import User, UserProfile
from domain.enums import UserRole
from repositories.interfaces import UserRepository
from core.exceptions import BusinessRuleError, NotFoundError
from core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for user management."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.logger = get_logger(self.__class__.__name__)
    
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        # Validate business rules
        await self._validate_user_creation(user)
        
        created_user = await self.user_repo.create(user)
        self.logger.info("User created", user_id=str(created_user.id), email=created_user.email)
        
        return created_user
    
    async def get_user(self, user_id: uuid.UUID) -> User:
        """Get user by ID."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return await self.user_repo.get_by_email(email)
    
    async def update_user(self, user: User) -> User:
        """Update user."""
        # Validate business rules
        await self._validate_user_update(user)
        
        updated_user = await self.user_repo.update(user)
        self.logger.info("User updated", user_id=str(updated_user.id))
        
        return updated_user
    
    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user."""
        success = await self.user_repo.delete(user_id)
        if success:
            self.logger.info("User deleted", user_id=str(user_id))
        else:
            self.logger.warning("Failed to delete user", user_id=str(user_id))
        
        return success
    
    async def list_users_by_role(self, role: str, limit: int = 100, offset: int = 0) -> List[User]:
        """List users by role."""
        return await self.user_repo.list_by_role(role, limit, offset)
    
    async def verify_user_age(self, user_id: uuid.UUID) -> User:
        """Verify user age."""
        user = await self.get_user(user_id)
        user.verify_age()
        updated_user = await self.user_repo.update(user)
        
        self.logger.info("User age verified", user_id=str(user_id))
        return updated_user
    
    async def update_last_login(self, user_id: uuid.UUID) -> User:
        """Update user's last login timestamp."""
        user = await self.get_user(user_id)
        user.update_last_login()
        updated_user = await self.user_repo.update(user)
        
        return updated_user
    
    async def deactivate_user(self, user_id: uuid.UUID) -> User:
        """Deactivate user account."""
        user = await self.get_user(user_id)
        user.is_active = False
        updated_user = await self.user_repo.update(user)
        
        self.logger.info("User deactivated", user_id=str(user_id))
        return updated_user
    
    async def activate_user(self, user_id: uuid.UUID) -> User:
        """Activate user account."""
        user = await self.get_user(user_id)
        user.is_active = True
        updated_user = await self.user_repo.update(user)
        
        self.logger.info("User activated", user_id=str(user_id))
        return updated_user
    
    def get_user_profile(self, user: User) -> UserProfile:
        """Convert User to UserProfile."""
        return UserProfile(
            id=user.id,
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            age_verified=user.age_verified,
            is_active=user.is_active,
            full_name=user.full_name,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
    
    async def _validate_user_creation(self, user: User) -> None:
        """Validate user creation business rules."""
        # Check if email already exists
        existing_user = await self.user_repo.get_by_email(user.email)
        if existing_user:
            raise BusinessRuleError(
                f"User with email {user.email} already exists",
                code="DUPLICATE_EMAIL"
            )
        
        # Validate role
        if user.role not in [UserRole.USER, UserRole.VENDOR, UserRole.ADMIN]:
            raise BusinessRuleError(
                f"Invalid user role: {user.role}",
                code="INVALID_ROLE"
            )
    
    async def _validate_user_update(self, user: User) -> None:
        """Validate user update business rules."""
        # Check if user exists
        existing = await self.user_repo.get_by_id(user.id)
        if not existing:
            raise NotFoundError(f"User with id {user.id} not found")
        
        # Check if email is being changed and if it conflicts
        if user.email != existing.email:
            email_user = await self.user_repo.get_by_email(user.email)
            if email_user and email_user.id != user.id:
                raise BusinessRuleError(
                    f"Email {user.email} is already in use",
                    code="DUPLICATE_EMAIL"
                )
