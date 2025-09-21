"""Domain enums and constants."""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    VENDOR = "vendor"
    ADMIN = "admin"


class VenueStatus(str, Enum):
    """Venue status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class LicenseType(str, Enum):
    """Venue license type enumeration."""
    RESTAURANT = "restaurant"
    BAR = "bar"
    PUB = "pub"
    BREWERY = "brewery"
    WINERY = "winery"
    DISTILLERY = "distillery"
    NIGHTCLUB = "nightclub"
    LOUNGE = "lounge"


class DayOfWeek(str, Enum):
    """Day of week enumeration."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class SecondaryHoursType(str, Enum):
    """Secondary hours type enumeration."""
    HAPPY_HOUR = "happy_hour"
    LATE_NIGHT = "late_night"
    BRUNCH = "brunch"
    PATIO = "patio"
    KITCHEN = "kitchen"


class DealCategory(str, Enum):
    """Deal category enumeration."""
    FOOD = "food"
    DRINK = "drink"
    BUNDLE = "bundle"
    EVENT = "event"


class PriceDisplayMode(str, Enum):
    """Price display mode enumeration."""
    HIDE = "hide"
    SHOW = "show"
    REDACT = "redact"


class MediaType(str, Enum):
    """Media type enumeration."""
    IMAGE = "image"
    MENU = "menu"
    LOGO = "logo"


class FlagStatus(str, Enum):
    """Flag status enumeration."""
    PENDING = "pending"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class FlagReason(str, Enum):
    """Flag reason enumeration."""
    OUTDATED_INFO = "outdated_info"
    INCORRECT_HOURS = "incorrect_hours"
    INCORRECT_PRICING = "incorrect_pricing"
    INAPPROPRIATE_CONTENT = "inappropriate_content"
    SPAM = "spam"
    OTHER = "other"


class EventType(str, Enum):
    """Analytics event type enumeration."""
    IMPRESSION = "impression"
    CLICK = "click"
    SAVE = "save"
    UNSAVE = "unsave"
    FLAG = "flag"
    SHARE = "share"
    CALL = "call"
    DIRECTIONS = "directions"
    WEBSITE_VISIT = "website_visit"


class Province(str, Enum):
    """Canadian province enumeration."""
    ON = "ON"  # Ontario
    BC = "BC"  # British Columbia
    AB = "AB"  # Alberta
    QC = "QC"  # Quebec
    NS = "NS"  # Nova Scotia
    NB = "NB"  # New Brunswick
    MB = "MB"  # Manitoba
    SK = "SK"  # Saskatchewan
    PE = "PE"  # Prince Edward Island
    NL = "NL"  # Newfoundland and Labrador
    YT = "YT"  # Yukon
    NT = "NT"  # Northwest Territories
    NU = "NU"  # Nunavut


# Province display names
PROVINCE_NAMES = {
    Province.ON: "Ontario",
    Province.BC: "British Columbia", 
    Province.AB: "Alberta",
    Province.QC: "Quebec",
    Province.NS: "Nova Scotia",
    Province.NB: "New Brunswick",
    Province.MB: "Manitoba",
    Province.SK: "Saskatchewan",
    Province.PE: "Prince Edward Island",
    Province.NL: "Newfoundland and Labrador",
    Province.YT: "Yukon",
    Province.NT: "Northwest Territories",
    Province.NU: "Nunavut",
}

# Initially supported provinces
SUPPORTED_PROVINCES = [Province.ON, Province.BC, Province.AB]
