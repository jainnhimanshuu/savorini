"""Route registration."""

from fastapi import FastAPI

from .routers import auth, deals, feed, meta, venues


def register_routes(app: FastAPI) -> None:
    """Register all API routes."""
    
    # Public routes
    app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
    app.include_router(meta.router, prefix="/v1/meta", tags=["meta"])
    app.include_router(feed.router, prefix="/v1/feed", tags=["feed"])
    
    # Resource routes
    app.include_router(venues.router, prefix="/v1/venues", tags=["venues"])
    app.include_router(deals.router, prefix="/v1/deals", tags=["deals"])
