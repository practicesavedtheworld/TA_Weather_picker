from typing import TypeAlias, Annotated

from sqlalchemy import sql
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.types import FLOAT, DECIMAL, INTEGER, DATETIME

Base: TypeAlias = DeclarativeBase
Now: TypeAlias = Annotated[DATETIME, mapped_column(default_factory=sql.func.now)]
Coordinates: TypeAlias = Annotated[FLOAT, mapped_column(nullable=True)]
SQL_FLOAT: TypeAlias = Annotated[FLOAT | DECIMAL, mapped_column(nullable=True, default=0.)]
SQL_INT: TypeAlias = Annotated[INTEGER, mapped_column(nullable=True, default=0)]
