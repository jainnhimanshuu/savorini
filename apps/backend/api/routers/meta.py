"""Metadata routes."""

from typing import Dict, List

from fastapi import APIRouter

from domain.entities import ProvinceRule, DEFAULT_PROVINCE_RULES
from domain.enums import Province, PROVINCE_NAMES, SUPPORTED_PROVINCES

router = APIRouter()


@router.get("/province-rules")
async def get_province_rules() -> Dict[str, ProvinceRule]:
    """Get province-specific rules and regulations."""
    return {
        province.value: rule.dict() 
        for province, rule in DEFAULT_PROVINCE_RULES.items()
        if province in SUPPORTED_PROVINCES
    }


@router.get("/provinces")
async def get_supported_provinces() -> List[Dict[str, str]]:
    """Get list of supported provinces."""
    return [
        {
            "code": province.value,
            "name": PROVINCE_NAMES[province],
            "supported": True,
        }
        for province in SUPPORTED_PROVINCES
    ]


@router.get("/cities")
async def get_cities(province: str = None) -> List[Dict[str, str]]:
    """Get list of cities, optionally filtered by province."""
    # TODO: Implement dynamic city lookup from database
    # For now, return mock data
    
    mock_cities = {
        "ON": [
            {"name": "Toronto", "province": "ON"},
            {"name": "Ottawa", "province": "ON"},
            {"name": "Hamilton", "province": "ON"},
            {"name": "London", "province": "ON"},
            {"name": "Kitchener", "province": "ON"},
        ],
        "BC": [
            {"name": "Vancouver", "province": "BC"},
            {"name": "Victoria", "province": "BC"},
            {"name": "Burnaby", "province": "BC"},
            {"name": "Richmond", "province": "BC"},
            {"name": "Surrey", "province": "BC"},
        ],
        "AB": [
            {"name": "Calgary", "province": "AB"},
            {"name": "Edmonton", "province": "AB"},
            {"name": "Red Deer", "province": "AB"},
            {"name": "Lethbridge", "province": "AB"},
            {"name": "Medicine Hat", "province": "AB"},
        ],
    }
    
    if province and province.upper() in mock_cities:
        return mock_cities[province.upper()]
    
    # Return all cities if no province specified
    all_cities = []
    for cities in mock_cities.values():
        all_cities.extend(cities)
    
    return all_cities


@router.get("/categories")
async def get_deal_categories() -> List[Dict[str, str]]:
    """Get list of deal categories."""
    from domain.enums import DealCategory
    
    return [
        {"code": category.value, "name": category.value.replace("_", " ").title()}
        for category in DealCategory
    ]


@router.get("/license-types")
async def get_license_types() -> List[Dict[str, str]]:
    """Get list of venue license types."""
    from domain.enums import LicenseType
    
    return [
        {"code": license_type.value, "name": license_type.value.replace("_", " ").title()}
        for license_type in LicenseType
    ]
