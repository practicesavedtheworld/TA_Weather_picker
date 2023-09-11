from os import PathLike
from typing import TypeAlias, Literal
import logging
import sys

LogLevel: TypeAlias = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def create_logger(logger_name: str,
                  logger_level: int | LogLevel = 20,
                  file_name: PathLike | str | None = None) -> logging.Logger:
    """"""
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
