"""Custom exception classes and error handlers."""

from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from .logging import get_logger

logger = get_logger(__name__)


class HappyHourException(Exception):
    """Base exception for Happy Hour application."""
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(HappyHourException):
    """Validation error."""
    pass


class NotFoundError(HappyHourException):
    """Resource not found error."""
    pass


class PermissionError(HappyHourException):
    """Permission denied error."""
    pass


class BusinessRuleError(HappyHourException):
    """Business rule violation error."""
    pass


class ExternalServiceError(HappyHourException):
    """External service error."""
    pass


def map_exception_to_http_status(exc: HappyHourException) -> int:
    """Map domain exceptions to HTTP status codes."""
    mapping = {
        ValidationError: status.HTTP_400_BAD_REQUEST,
        NotFoundError: status.HTTP_404_NOT_FOUND,
        PermissionError: status.HTTP_403_FORBIDDEN,
        BusinessRuleError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        ExternalServiceError: status.HTTP_503_SERVICE_UNAVAILABLE,
    }
    return mapping.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)


async def happyhour_exception_handler(
    request: Request, 
    exc: HappyHourException
) -> JSONResponse:
    """Handle custom application exceptions."""
    status_code = map_exception_to_http_status(exc)
    
    logger.error(
        "Application exception",
        exception=exc.__class__.__name__,
        message=exc.message,
        code=exc.code,
        details=exc.details,
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    logger.warning(
        "HTTP exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": {},
            }
        },
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Pydantic validation exceptions."""
    logger.warning(
        "Validation exception",
        error=str(exc),
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": {"validation_error": str(exc)},
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(
        "Unhandled exception",
        exception=exc.__class__.__name__,
        error=str(exc),
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            }
        },
    )
