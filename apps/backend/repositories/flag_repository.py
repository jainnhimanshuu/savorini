"""Flag repository implementation."""

import uuid
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Flag
from domain.enums import FlagStatus
from repositories.base import BaseRepository
from repositories.models import Flag as FlagModel


class FlagRepositoryImpl(BaseRepository[Flag, FlagModel]):
    """Flag repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, FlagModel)
    
    async def list_pending(self, limit: int = 50, offset: int = 0) -> List[Flag]:
        """List pending flags."""
        result = await self.db.execute(
            select(FlagModel)
            .where(FlagModel.status == FlagStatus.PENDING)
            .offset(offset)
            .limit(limit)
            .order_by(FlagModel.created_at.desc())
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: Flag) -> FlagModel:
        """Convert Flag entity to FlagModel."""
        return FlagModel(
            id=entity.id,
            target_type=entity.target_type,
            target_id=entity.target_id,
            reason=entity.reason,
            description=entity.description,
            user_id=entity.user_id,
            status=entity.status,
            resolved_by=entity.resolved_by,
            resolved_at=entity.resolved_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: FlagModel) -> Flag:
        """Convert FlagModel to Flag entity."""
        return Flag(
            id=model.id,
            target_type=model.target_type,
            target_id=model.target_id,
            reason=model.reason,
            description=model.description,
            user_id=model.user_id,
            status=model.status,
            resolved_by=model.resolved_by,
            resolved_at=model.resolved_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
