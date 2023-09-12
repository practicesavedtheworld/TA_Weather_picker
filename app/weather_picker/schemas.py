from typing import TypeAlias
import decimal

from pydantic import BaseModel

Float: TypeAlias = float | decimal.Decimal


class Coordinates(BaseModel):
    lat: float
    lon: float


class Weather(BaseModel):
    description: str
    icon: str
    id: int
    main: str


class WeatherDataSchemeFromOpenWeather(BaseModel):
    base: str
    clouds: dict[str, int]
    coord: Coordinates
    dt: int
    id: int
    main: dict[str, int | Float]
    name: str
    sys: dict
    timezone: int
    visibility: int
    weather: list[Weather]
    wind: dict[str, int | Float]