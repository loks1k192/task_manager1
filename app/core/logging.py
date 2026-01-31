"""Logging configuration."""

import logging
import sys

import structlog
from structlog.types import Processor

from app.core.config import settings


def setup_logging() -> None:
    """Setup structured logging."""
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    if settings.DEBUG:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(),
            ]
        )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(settings.LOG_LEVEL)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
