"""User repository implementation."""

import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import User
from domain.enums import UserRole
from repositories.base import BaseRepository
from repositories.models import User as UserModel


class UserRepositoryImpl(BaseRepository[User, UserModel]):
    """User repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserModel)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_obj = result.scalar_one_or_none()
        return self._model_to_entity(db_obj) if db_obj else None
    
    async def list_by_role(self, role: str, limit: int = 100, offset: int = 0) -> List[User]:
        """List users by role."""
        result = await self.db.execute(
            select(UserModel)
            .where(UserModel.role == UserRole(role))
            .offset(offset)
            .limit(limit)
            .order_by(UserModel.created_at.desc())
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: User) -> UserModel:
        """Convert User entity to UserModel."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            provider_sub=entity.provider_sub,
            role=entity.role,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone=entity.phone,
            age_verified=entity.age_verified,
            is_active=entity.is_active,
            last_login_at=entity.last_login_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity."""
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            provider_sub=model.provider_sub,
            role=model.role,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            age_verified=model.age_verified,
            is_active=model.is_active,
            last_login_at=model.last_login_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
