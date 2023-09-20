import pytest

from app.exceptions import NoCitiesSelected


class TestCities:

    @pytest.mark.parametrize(
        "quantity",
        [
            2,
            10,
            20,
            100,
        ],
    )
    def test_city_data(self, cities_instance, quantity):
        cities = cities_instance.get_largest_cities_names(quantity=quantity)
        assert len(cities) == quantity and all(
            map(
                lambda c: isinstance(c, str),
                cities,
            )
        )

    @pytest.mark.parametrize(
        "quantity",
        [
            -2,
            0,
            -1123,
            0.0,
        ],
    )
    def test_no_city(self, cities_instance, quantity):
        with pytest.raises(NoCitiesSelected):
            cities_instance.get_largest_cities_names(quantity=quantity)