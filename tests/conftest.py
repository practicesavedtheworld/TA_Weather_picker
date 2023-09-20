from pytest import fixture

from app.cities import cities
from app.config import settings


@fixture()
def api_key():
    return settings.OPENWEATHERAPI_KEY


@fixture()
def cities_instance():
    return cities
