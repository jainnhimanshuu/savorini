"""Compliance service for province-specific rules."""

from typing import Dict, Optional

from domain.entities import Deal, ProvinceRule, DEFAULT_PROVINCE_RULES
from domain.enums import PriceDisplayMode, Province, UserRole
from core.exceptions import BusinessRuleError
from core.logging import get_logger

logger = get_logger(__name__)


class ComplianceService:
    """Service for applying province-specific compliance rules."""
    
    def __init__(self):
        self.rules_cache: Dict[Province, ProvinceRule] = DEFAULT_PROVINCE_RULES.copy()
        self.logger = get_logger(self.__class__.__name__)
    
    def get_province_rule(self, province: Province) -> ProvinceRule:
        """Get province rule, with fallback to default."""
        if province in self.rules_cache:
            return self.rules_cache[province]
        
        # Fallback to Ontario rules if province not found
        self.logger.warning(f"No rules found for province {province}, using ON fallback")
        return self.rules_cache[Province.ON]
    
    def apply_price_display_rules(
        self, 
        deal: Deal, 
        province: Province, 
        user_role: Optional[UserRole] = None
    ) -> Deal:
        """Apply province-specific price display rules to a deal."""
        rule = self.get_province_rule(province)
        
        # Admins and vendors can always see prices
        if user_role in [UserRole.ADMIN, UserRole.VENDOR]:
            deal.price_display_mode = PriceDisplayMode.SHOW
            return deal
        
        # Apply province rules for regular users
        if not rule.allow_price_display:
            if rule.hide_alcohol_prices and self._is_alcohol_deal(deal):
                deal.price_display_mode = PriceDisplayMode.HIDE
            else:
                deal.price_display_mode = PriceDisplayMode.REDACT
        else:
            deal.price_display_mode = PriceDisplayMode.SHOW
        
        return deal
    
    def validate_deal_compliance(self, deal: Deal, province: Province) -> None:
        """Validate deal compliance with province rules."""
        rule = self.get_province_rule(province)
        
        # Check age verification requirements
        if self._is_alcohol_deal(deal) and rule.require_age_verification:
            if not deal.requires_age_verification:
                raise BusinessRuleError(
                    f"Alcohol deals in {province.value} require age verification",
                    code="AGE_VERIFICATION_REQUIRED"
                )
        
        # Check discount limits
        if rule.max_discount_percentage and deal.savings_percentage:
            if deal.savings_percentage > rule.max_discount_percentage:
                raise BusinessRuleError(
                    f"Discount exceeds maximum allowed in {province.value} "
                    f"({rule.max_discount_percentage}%)",
                    code="DISCOUNT_LIMIT_EXCEEDED"
                )
        
        # Check happy hour marketing restrictions
        if not rule.allow_happy_hour_marketing:
            if "happy hour" in deal.title.lower() or "happy hour" in (deal.description or "").lower():
                raise BusinessRuleError(
                    f"Happy hour marketing not allowed in {province.value}",
                    code="HAPPY_HOUR_MARKETING_RESTRICTED"
                )
    
    def get_disclaimer_text(self, province: Province) -> Optional[str]:
        """Get province-specific disclaimer text."""
        rule = self.get_province_rule(province)
        return rule.disclaimer
    
    def is_age_verification_required(self, deal: Deal, province: Province) -> bool:
        """Check if age verification is required for this deal."""
        rule = self.get_province_rule(province)
        return rule.require_age_verification and self._is_alcohol_deal(deal)
    
    def _is_alcohol_deal(self, deal: Deal) -> bool:
        """Check if deal involves alcohol."""
        alcohol_keywords = [
            "beer", "wine", "cocktail", "drink", "alcohol", "spirits", 
            "whiskey", "vodka", "gin", "rum", "tequila", "liqueur",
            "bar", "pub", "brewery", "winery", "distillery"
        ]
        
        text_to_check = f"{deal.title} {deal.description or ''}".lower()
        return any(keyword in text_to_check for keyword in alcohol_keywords)
    
    def redact_price_info(self, deal: Deal) -> Deal:
        """Redact price information from deal."""
        if deal.price_display_mode == PriceDisplayMode.HIDE:
            deal.original_price = None
            deal.deal_price = None
        elif deal.price_display_mode == PriceDisplayMode.REDACT:
            # Keep prices but add disclaimer
            pass
        
        return deal
    
    def update_rules_cache(self, rules: Dict[Province, ProvinceRule]) -> None:
        """Update the rules cache (for admin updates)."""
        self.rules_cache.update(rules)
        self.logger.info("Province rules cache updated", provinces=list(rules.keys()))
