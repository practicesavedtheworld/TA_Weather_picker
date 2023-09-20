from datetime import datetime

from pydantic import BaseModel, Field

from app.types import Float, FLOAT_OR_INT


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
    main: dict[str, FLOAT_OR_INT]
    name: str
    sys: dict
    timezone: int
    visibility: int
    weather: list[Weather]
    wind: dict[str, FLOAT_OR_INT]


class CityModelScheme(BaseModel):
    name: str
    longitude: Float
    latitude: Float
    country: str


class CityTimestampScheme(BaseModel):
    city_id: int
    created_at: datetime
    updated_at: datetime


class MainWeatherScheme(BaseModel):
    city_id: int
    feels_like: Float
    grnd_level: int
    humidity: int
    pressure: int
    sea_level: int
    temp: Float
    temp_max: Float
    temp_min: Float


class ExtraWeatherScheme(BaseModel):
    city_id: int
    visibility: int
    wind: dict[str, FLOAT_OR_INT]
    recorded_at: datetime
