from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.types import SQL_FLOAT, Base, Coordinates, Now, SQL_INT


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

    city_id: Mapped[Annotated[int, mapped_column(ForeignKey("city.id"))]]
    feels_like: Mapped[SQL_FLOAT]
    grnd_level: Mapped[SQL_INT]
    humidity: Mapped[SQL_INT]
    pressure: Mapped[SQL_INT]
    sea_level: Mapped[SQL_INT]
    temp: Mapped[SQL_FLOAT]
    temp_max: Mapped[SQL_FLOAT]
    temp_min: Mapped[SQL_FLOAT]


class ExtraWeather(BaseWeather):
    __tablename__ = "extra_weather"
