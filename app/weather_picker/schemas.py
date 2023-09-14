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


class WindCondition:
    degree: FLOAT_OR_INT = Field(default=0, ge=0, lt=361)
    gust: FLOAT_OR_INT = Field(default=0., ge=0)
    speed: FLOAT_OR_INT = Field(ge=0)
