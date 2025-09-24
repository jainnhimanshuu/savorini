"""Media repository implementation."""

import uuid
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Media
from domain.enums import MediaType
from repositories.base import BaseRepository
from repositories.models import Media as MediaModel


class MediaRepositoryImpl(BaseRepository[Media, MediaModel]):
    """Media repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, MediaModel)
    
    async def list_by_venue(self, venue_id: uuid.UUID, media_type: Optional[str] = None) -> List[Media]:
        """List media by venue."""
        conditions = [MediaModel.venue_id == venue_id, MediaModel.is_active == True]
        
        if media_type:
            conditions.append(MediaModel.type == MediaType(media_type))
        
        result = await self.db.execute(
            select(MediaModel)
            .where(and_(*conditions))
            .order_by(MediaModel.display_order, MediaModel.created_at)
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: Media) -> MediaModel:
        """Convert Media entity to MediaModel."""
        return MediaModel(
            id=entity.id,
            venue_id=entity.venue_id,
            type=entity.type,
            uri=entity.uri,
            alt_text=entity.alt_text,
            caption=entity.caption,
            filename=entity.filename,
            file_size=entity.file_size,
            mime_type=entity.mime_type,
            width=entity.width,
            height=entity.height,
            is_primary=entity.is_primary,
            display_order=entity.display_order,
            is_active=entity.is_active,
            uploaded_by=entity.uploaded_by,
            original_filename=entity.original_filename,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: MediaModel) -> Media:
        """Convert MediaModel to Media entity."""
        return Media(
            id=model.id,
            venue_id=model.venue_id,
            type=model.type,
            uri=model.uri,
            alt_text=model.alt_text,
            caption=model.caption,
            filename=model.filename,
            file_size=model.file_size,
            mime_type=model.mime_type,
            width=model.width,
            height=model.height,
            is_primary=model.is_primary,
            display_order=model.display_order,
            is_active=model.is_active,
            uploaded_by=model.uploaded_by,
            original_filename=model.original_filename,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
