"""Favorite repository implementation."""

import uuid
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Favorite
from repositories.base import BaseRepository
from repositories.models import Favorite as FavoriteModel


class FavoriteRepositoryImpl(BaseRepository[Favorite, FavoriteModel]):
    """Favorite repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, FavoriteModel)
    
    async def get_by_user_and_venue(self, user_id: uuid.UUID, venue_id: uuid.UUID) -> Optional[Favorite]:
        """Get favorite by user and venue."""
        result = await self.db.execute(
            select(FavoriteModel).where(
                and_(
                    FavoriteModel.user_id == user_id,
                    FavoriteModel.venue_id == venue_id
                )
            )
        )
        db_obj = result.scalar_one_or_none()
        return self._model_to_entity(db_obj) if db_obj else None
    
    async def list_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[Favorite]:
        """List favorites by user."""
        result = await self.db.execute(
            select(FavoriteModel)
            .where(FavoriteModel.user_id == user_id)
            .offset(offset)
            .limit(limit)
            .order_by(FavoriteModel.created_at.desc())
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: Favorite) -> FavoriteModel:
        """Convert Favorite entity to FavoriteModel."""
        return FavoriteModel(
            id=entity.id,
            user_id=entity.user_id,
            venue_id=entity.venue_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: FavoriteModel) -> Favorite:
        """Convert FavoriteModel to Favorite entity."""
        return Favorite(
            id=model.id,
            user_id=model.user_id,
            venue_id=model.venue_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
