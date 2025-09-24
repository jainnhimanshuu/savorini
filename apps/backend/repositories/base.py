"""Base repository implementation."""

import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)
ModelType = TypeVar("ModelType")


class BaseRepository(Generic[T, ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        db_obj = self._entity_to_model(entity)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return self._model_to_entity(db_obj)
    
    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[T]:
        """Get entity by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        db_obj = result.scalar_one_or_none()
        return self._model_to_entity(db_obj) if db_obj else None
    
    async def update(self, entity: T) -> T:
        """Update entity."""
        db_obj = await self.db.get(self.model, entity.id)
        if not db_obj:
            raise ValueError(f"Entity with id {entity.id} not found")
        
        # Update fields
        for field, value in entity.model_dump(exclude_unset=True).items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.db.flush()
        await self.db.refresh(db_obj)
        return self._model_to_entity(db_obj)
    
    async def delete(self, entity_id: uuid.UUID) -> bool:
        """Delete entity."""
        db_obj = await self.db.get(self.model, entity_id)
        if not db_obj:
            return False
        
        await self.db.delete(db_obj)
        await self.db.flush()
        return True
    
    async def list(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """List entities with pagination and filtering."""
        query = select(self.model)
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    if isinstance(value, list):
                        query = query.where(getattr(self.model, field).in_(value))
                    else:
                        query = query.where(getattr(self.model, field) == value)
        
        # Apply ordering
        if order_by:
            if order_by.startswith("-"):
                query = query.order_by(desc(getattr(self.model, order_by[1:])))
            else:
                query = query.order_by(getattr(self.model, order_by))
        else:
            query = query.order_by(desc(self.model.created_at))
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: T) -> ModelType:
        """Convert domain entity to SQLAlchemy model."""
        # This should be implemented by subclasses
        raise NotImplementedError
    
    def _model_to_entity(self, model: ModelType) -> T:
        """Convert SQLAlchemy model to domain entity."""
        # This should be implemented by subclasses
        raise NotImplementedError
