import datetime
import decimal
from typing import TypeAlias, Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import sql, ForeignKey

Base: TypeAlias = DeclarativeBase
Now: TypeAlias = Annotated[datetime.datetime, mapped_column(default_factory=sql.func.now)]
Float: TypeAlias = float | decimal.Decimal
Coordinates: TypeAlias = Annotated[float, mapped_column(
    nullable=True)]


class BaseWeather(Base):
    __abstract__ = True

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]


class CityModel(BaseWeather):
    __tablename__ = "city"

    name: Mapped[Annotated[str, mapped_column(nullable=False)]]
    longitude: Mapped[Coordinates]
    latitude: Mapped[Coordinates]
    country: Mapped[Annotated[str, mapped_column(nullable=True)]]


class CityTimestamp:
    __tablename__ = "city_timestamp"

    city_id: Mapped[Annotated[int, mapped_column(ForeignKey("city.id"))]]
    created_at: Mapped[Now]
    updated_at: Mapped[Now]


class MainWeather(BaseWeather):
    __tablename__ = "main_weather"


class ExtraWeather(BaseWeather):
    __tablename__ = "extra_weather"
