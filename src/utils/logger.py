"""
Logging configuration for MDxApp.
Provides structured logging with different levels and formatters.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "mdxapp",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_json: bool = False,
) -> logging.Logger:
    """
    Configure and return a logger instance with consistent formatting.

    Args:
        name: Logger name (default: "mdxapp")
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        format_json: Use JSON formatting (default: False)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    if format_json:
        # JSON format for structured logging (future enhancement)
        log_format = '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
    else:
        # Human-readable format
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(log_format)

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "mdxapp") -> logging.Logger:
    """
    Get or create a logger instance.

    Args:
        name: Logger name

    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)

    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        return setup_logger(name)

    return logger
