"""
QBot - AI-Powered Q&A Bot using Ollama and Vector Store
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Dict, Any

# Version information
__version__ = "0.1.0"
__author__ = "Your Name"
__author_email__ = "your.email@example.com"


# Setup logging configuration
def setup_logging(
        log_level: str = "INFO",
        log_file: str = "qbot.log",
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5
) -> logging.Logger:
    """
    Configure logging for QBot.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Setup file handler with rotation
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Setup logger
    logger = logging.getLogger('qbot')
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create default logger
logger = setup_logging()


def get_version() -> str:
    """Return the current version of QBot."""
    return __version__


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration of QBot.

    Returns:
        Dict containing configuration settings
    """
    from .config import (
        OLLAMA_HOST,
        OLLAMA_PORT,
        DEFAULT_MODEL,
        EMBEDDING_MODEL
    )

    return {
        "ollama_host": OLLAMA_HOST,
        "ollama_port": OLLAMA_PORT,
        "default_model": DEFAULT_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "version": __version__
    }


class QBotException(Exception):
    """Base exception class for QBot."""
    pass


class ModelNotFoundError(QBotException):
    """Raised when a required model is not found."""
    pass


class ConfigurationError(QBotException):
    """Raised when there's a configuration error."""
    pass


class VectorStoreError(QBotException):
    """Raised when there's an error with the vector store."""
    pass


# Import main components for easier access
from .models.vector_store import VectorStore
from .utils.helpers import format_response, validate_prompt

__all__ = [
    'VectorStore',
    'format_response',
    'validate_prompt',
    'setup_logging',
    'get_version',
    'get_config',
    'QBotException',
    'ModelNotFoundError',
    'ConfigurationError',
    'VectorStoreError',
    'logger'
]