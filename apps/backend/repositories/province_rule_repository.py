"""Province rule repository implementation."""

import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import ProvinceRule
from domain.enums import Province
from repositories.base import BaseRepository
from repositories.models import ProvinceRule as ProvinceRuleModel


class ProvinceRuleRepositoryImpl(BaseRepository[ProvinceRule, ProvinceRuleModel]):
    """Province rule repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, ProvinceRuleModel)
    
    async def get_by_province(self, province: str) -> Optional[ProvinceRule]:
        """Get province rule by province."""
        result = await self.db.execute(
            select(ProvinceRuleModel).where(ProvinceRuleModel.province == Province(province))
        )
        db_obj = result.scalar_one_or_none()
        return self._model_to_entity(db_obj) if db_obj else None
    
    async def list_all(self) -> List[ProvinceRule]:
        """List all province rules."""
        result = await self.db.execute(
            select(ProvinceRuleModel).order_by(ProvinceRuleModel.province)
        )
        db_objects = result.scalars().all()
        return [self._model_to_entity(obj) for obj in db_objects]
    
    def _entity_to_model(self, entity: ProvinceRule) -> ProvinceRuleModel:
        """Convert ProvinceRule entity to ProvinceRuleModel."""
        return ProvinceRuleModel(
            id=entity.id,
            province=entity.province,
            allow_price_display=entity.allow_price_display,
            brand_logo_ok=entity.brand_logo_ok,
            disclaimer=entity.disclaimer,
            require_age_verification=entity.require_age_verification,
            min_age=entity.min_age,
            hide_alcohol_brands=entity.hide_alcohol_brands,
            hide_alcohol_prices=entity.hide_alcohol_prices,
            require_food_with_alcohol=entity.require_food_with_alcohol,
            alcohol_sales_start_time=entity.alcohol_sales_start_time,
            alcohol_sales_end_time=entity.alcohol_sales_end_time,
            allow_happy_hour_marketing=entity.allow_happy_hour_marketing,
            max_discount_percentage=entity.max_discount_percentage,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _model_to_entity(self, model: ProvinceRuleModel) -> ProvinceRule:
        """Convert ProvinceRuleModel to ProvinceRule entity."""
        return ProvinceRule(
            id=model.id,
            province=model.province,
            allow_price_display=model.allow_price_display,
            brand_logo_ok=model.brand_logo_ok,
            disclaimer=model.disclaimer,
            require_age_verification=model.require_age_verification,
            min_age=model.min_age,
            hide_alcohol_brands=model.hide_alcohol_brands,
            hide_alcohol_prices=model.hide_alcohol_prices,
            require_food_with_alcohol=model.require_food_with_alcohol,
            alcohol_sales_start_time=model.alcohol_sales_start_time,
            alcohol_sales_end_time=model.alcohol_sales_end_time,
            allow_happy_hour_marketing=model.allow_happy_hour_marketing,
            max_discount_percentage=model.max_discount_percentage,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
