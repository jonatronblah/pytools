import logging
from pathlib import Path
from pytools.config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(settings.logging.level)

        # Create formatter
        formatter = logging.Formatter(settings.logging.format)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if configured)
        if settings.logging.file_path:
            file_path = Path(settings.logging.file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
