
import logging
import os
from pathlib import Path


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "skillforge.log"


def get_logger(name: str) -> logging.Logger:
    """
    Create or retrieve a configured logger.

    Logs are written to the console and to logs/skillforge.log.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = getattr(logging, LOG_LEVEL, logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except OSError:
        # Console logging remains available if file logging fails.
        pass

    return logger
