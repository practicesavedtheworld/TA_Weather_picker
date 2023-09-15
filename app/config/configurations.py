from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config import create_logger

BASE_DIR: Path = Path(__file__).parent.parent.parent
logger = create_logger(
    "settings_logger",
    logger_level="INFO",
)


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: str | None = None

    model_config = SettingsConfigDict(
        #  File priority direction is from right to left side
        #  So the first file for search would be .test_env
        #  The direction must change closer to release.
        env_file=[f"{BASE_DIR}.env", f"{BASE_DIR}.test_env"],
        env_file_encoding="UTF-8"
    )

    def __init__(self: Self, **kwargs):
        """
        Creating a DB_URL attribute after initialization (after all
        the env-vars have been parsed, it will be initialized.)
        After the initialization method creates the DB_URL attribute."""

        s: Self = self
        super().__init__(**kwargs)
        db_driver_info = "postgresql+asyncpg://"
        db_params = f"{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"
        s.DB_URL = f"{db_driver_info}{db_params}"


try:
    settings = Settings()
    logger.info("Settings parse complete")
except:
    logger.critical("Settings does not match. Further application normal work is impossible")
    # TODO  add custom exception