"""Logging configuration for the application."""

import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""

    # Set log level for root logger
    logging.root.setLevel(log_level)

    # Remove default handlers and add InterceptHandler
    logging.root.handlers = [InterceptHandler()]

    # Set log levels for libraries
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).propagate = True

    # Configure handlers format based on log level
    if logging.root.level <= 10:
        handlers = [
            {
                "sink": sys.stdout,
                "level": log_level,
                "format": "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> | <level>{level: <8}</level> | <y>{name}:{line}</y> | <level>{message}</level>",
            },
        ]
    else:
        handlers = [
            {
                "sink": sys.stdout,
                "level": log_level,
                "format": "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> | <level>{level: <8}</level> | <level>{message}</level>",
            },
        ]

    # Configure loguru
    logger.configure(handlers=handlers)
