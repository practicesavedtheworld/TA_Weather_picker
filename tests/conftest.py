from pytest import fixture

from app.cities import cities

@fixture()
def cities_instance():
    return cities


