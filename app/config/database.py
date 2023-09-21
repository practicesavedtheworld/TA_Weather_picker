from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import create_logger, settings
from app.types import connected

logger = create_logger(
    logger_name="database_logger",
    logger_level="DEBUG",
)

try:
    async_engine: AsyncEngine = create_async_engine(settings.DB_URL)
    session: AsyncSession = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
    )()  # type ignore
    logger.info("Create engine. Ready to use")
    connected = True
except SQLAlchemyError as db_err:
    connected = False
    logger.critical(
        "Won't able connect to database. There is some problem occur", exc_info=db_err
    )
finally:
    logger.debug(f"Connect to database. Status {'success' if connected else 'failed'}")
