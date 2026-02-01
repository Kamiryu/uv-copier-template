"""Logging configuration with Rich console output and file handling."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterable

form rich.logging import RichHandler

DEFAULT_LOG_FORMAT = "%(message)s"
FILE_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(
    log_level: str,
    log_file: str | Path,
    *,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
    handlers: Iterable[logging.Handler] | None = None,
) -> None:
    """Configure logging with Rich console output and a rotating file handler."""

    level = log_level.upper()

    if handlers is None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))

        handlers = [
            RichHandler(rich_tracebacks=True),
            file_handler,
        ]

    logging.basicConfig(
        level=level,
        format=DEFAULT_LOG_FORMAT,
        datefmt="[%X]",
        handlers=list(handlers),
    )