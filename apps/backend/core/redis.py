"""Redis configuration and client management."""

from typing import Optional

import redis.asyncio as redis

from .config import get_settings
from .logging import get_logger

logger = get_logger(__name__)

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis client."""
    global redis_client
    
    settings = get_settings()
    
    redis_client = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        health_check_interval=30,
    )
    
    # Test connection
    await redis_client.ping()
    logger.info("Redis initialized", redis_url=settings.redis_url)


async def get_redis() -> redis.Redis:
    """Get Redis client dependency."""
    if redis_client is None:
        raise RuntimeError("Redis not initialized")
    return redis_client


async def close_redis() -> None:
    """Close Redis connections."""
    global redis_client
    
    if redis_client:
        await redis_client.close()
        logger.info("Redis connections closed")


class CacheManager:
    """Redis cache manager with common patterns."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.logger = get_logger(self.__class__.__name__)
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        try:
            return await self.redis.get(key)
        except Exception as e:
            self.logger.warning("Cache get failed", key=key, error=str(e))
            return None
    
    async def set(
        self, 
        key: str, 
        value: str, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        try:
            return await self.redis.set(key, value, ex=ttl)
        except Exception as e:
            self.logger.warning("Cache set failed", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            return bool(await self.redis.delete(key))
        except Exception as e:
            self.logger.warning("Cache delete failed", key=key, error=str(e))
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            self.logger.warning("Cache delete pattern failed", pattern=pattern, error=str(e))
            return 0
