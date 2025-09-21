"""Database configuration and session management."""

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import get_settings
from .logging import get_logger

logger = get_logger(__name__)

# Database metadata and base
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Global engine and session factory
engine = None
async_session_factory = None


async def init_database() -> None:
    """Initialize database engine and session factory."""
    global engine, async_session_factory
    
    settings = get_settings()
    
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    logger.info("Database initialized", database_url=settings.database_url)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    if async_session_factory is None:
        raise RuntimeError("Database not initialized")
    
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_database() -> None:
    """Close database connections."""
    global engine
    
    if engine:
        await engine.dispose()
        logger.info("Database connections closed")
