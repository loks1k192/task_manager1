"""Global exception handlers."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from structlog import get_logger

logger = get_logger()


class TaskNotFoundError(Exception):
    """Task not found exception."""

    pass


class UserNotFoundError(Exception):
    """User not found exception."""

    pass


class UnauthorizedError(Exception):
    """Unauthorized exception."""

    pass


class ValidationError(Exception):
    """Validation exception."""

    pass


async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    """Handle TaskNotFoundError."""
    logger.warning("Task not found", path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Task not found"},
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    """Handle UserNotFoundError."""
    logger.warning("User not found", path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"},
    )


async def unauthorized_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handle UnauthorizedError."""
    logger.warning("Unauthorized access", path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Unauthorized"},
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle ValidationError."""
    logger.warning("Validation error", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle SQLAlchemy IntegrityError."""
    logger.error("Database integrity error", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database integrity error"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions."""
    logger.exception("Unhandled exception", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers for the application."""
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
