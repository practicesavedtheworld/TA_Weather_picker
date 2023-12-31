import logging
import sys
from os import PathLike

from app.types import LogLevel


def create_logger(
    logger_name: str,
    logger_level: int | LogLevel = 20,
    file_name: PathLike | str | None = None,
) -> logging.Logger:
    """Create flexible logger, that can handle with different levels. Also,
    it can write log into the file or stdout."""

    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    if file_name:
        handler = logging.FileHandler(filename=file_name, encoding="UTF-8")
    else:
        handler = logging.StreamHandler(stream=sys.stdout)

    logger_formatter = logging.Formatter("%(asctime)s - %(levelname)s  - %(message)s")
    handler.setFormatter(logger_formatter)
    handler.setLevel(logger_level)
    logger.addHandler(handler)

    return logger
