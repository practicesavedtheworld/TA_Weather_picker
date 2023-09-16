import datetime
from typing import TypeAlias, Annotated

from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, declarative_base


Base: TypeAlias = declarative_base()  # For some reason DeclarativeBase didn't work.
Now: TypeAlias = Annotated[datetime.datetime, mapped_column(default_factory=sql.func.now)]
Coordinates: TypeAlias = Annotated[float, mapped_column(nullable=True)]
SQL_FLOAT: TypeAlias = Annotated[float, mapped_column(nullable=True, default=0.)]
SQL_INT: TypeAlias = Annotated[int, mapped_column(nullable=True, default=0)]
SQL_JSON: TypeAlias = Annotated[JSONB, mapped_column(JSONB, default={})]
