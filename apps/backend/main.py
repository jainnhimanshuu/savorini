"""Main FastAPI application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from api.routes import register_routes
from core.config import get_settings
from core.database import close_database, init_database
from core.exceptions import (
    HappyHourException,
    generic_exception_handler,
    happyhour_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from core.logging import LoggingMiddleware, setup_logging
from core.redis import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    setup_logging()
    await init_database()
    await init_redis()
    
    yield
    
    # Shutdown
    await close_database()
    await close_redis()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Happy Hour Finder API",
        description="API for discovering happy hour deals across Canada",
        version="1.0.0",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )
    
    # Rate limiting
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.rate_limit_requests}/minute"],
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Middleware
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    app.add_exception_handler(HappyHourException, happyhour_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValueError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    # Routes
    register_routes(app)
    
    # Health check
    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse({"status": "healthy", "version": "1.0.0"})
    
    return app


# Create app instance
app = create_app()
