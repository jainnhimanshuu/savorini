"""Application configuration using Pydantic settings."""

from functools import lru_cache
from typing import List, Union, Any
import json

from pydantic import Field, field_validator, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic_settings import BaseSettings, SettingsConfigDict


class AllowedOriginsType:
    """Custom type for handling allowed origins with flexible parsing."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "array", "items": {"type": "string"}}
    
    @classmethod
    def _validate(cls, value: Any) -> List[str]:
        """Validate and parse allowed origins from various formats."""
        if isinstance(value, list):
            return value
        
        if isinstance(value, str):
            if not value.strip():
                return ["http://localhost:3000", "http://localhost:3001", "http://localhost:8081"]
            
            # Try to parse as JSON first
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            
            # If JSON parsing fails, treat as comma-separated string
            return [origin.strip() for origin in value.split(',') if origin.strip()]
        
        # Default fallback
        return ["http://localhost:3000", "http://localhost:3001", "http://localhost:8081"]


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Ignore empty environment variables to prevent JSON parsing errors
        env_ignore_empty=True,
        # Use custom parsing for complex types
        env_parse_none_str="",
    )
    
    # App
    app_name: str = "Happy Hour Finder API"
    version: str = "1.0.0"
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO")
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/happyhour"
    )
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # Security
    jwt_secret_key: str = Field(default="your-secret-key-change-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    jwt_refresh_token_expire_days: int = Field(default=7)
    
    # CORS
    allowed_origins: AllowedOriginsType = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:8081"
        ]
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100)
    rate_limit_window: int = Field(default=60)
    
    # External Services
    google_places_api_key: str = Field(default="")
    sendgrid_api_key: str = Field(default="")
    expo_access_token: str = Field(default="")
    
    # Object Storage
    s3_bucket: str = Field(default="happyhour-media")
    s3_region: str = Field(default="us-east-1")
    s3_access_key_id: str = Field(default="")
    s3_secret_access_key: str = Field(default="")
    s3_endpoint_url: str = Field(default="https://s3.amazonaws.com")
    
    # Monitoring
    sentry_dsn: str = Field(default="")
    opentelemetry_endpoint: str = Field(default="http://localhost:4317")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
