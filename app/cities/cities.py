import functools
from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Optional

import geonamescache

from app.config import create_logger
from app.exceptions import NoCitiesSelected

logger = create_logger(
    logger_name="cities_logger",
    logger_level="DEBUG",
)


class WorldCities(ABC):
    _cities_instance: Optional["WorldCities"] = None

    def __new__(cls, *args, **kwargs):
        if cls._cities_instance is None:
            cls._cities_instance = super().__new__(cls)
            cls._cities_instance.world_cities = (
                geonamescache.GeonamesCache().get_cities()
            )
        return cls._cities_instance

    @staticmethod
    def sort_cities_by_population(cities_seq: Iterable) -> list[dict]:
        """Sorting cities by population"""

        return sorted(
            cities_seq,
            key=lambda cur_city: cur_city["population"],
        )

    @abstractmethod
    def get_largest_cities_by_quantity(self, quantity: int):
        ...


class Cities(WorldCities):
    def get_largest_cities_by_quantity(
        self, quantity: int = 100, min_population: int = 1_000_000
    ) -> list[dict]:
        """Receive the largest cities in the world according to
        geonamescache library data.

        According to the Earth population ~8_000_000_000, min_population
        param default is 1_000_000.
        When you need more that top 1000 cities, you may need to decrease
        the min_population param.
        The more cities you get, the less min_population you set"""
        try:
            assert quantity > 0
        except AssertionError:
            raise NoCitiesSelected(
                exc_details=f"Your city quantity is {quantity}. Change it"
            )
        largest_cities: Iterator[dict] = (
            city
            for city in self.world_cities.values()
            if city["population"] >= min_population
        )
        logger.debug(f"Successfully receive {quantity} largest city")
        return self.sort_cities_by_population(largest_cities)[-quantity:]

    @functools.lru_cache(maxsize=20)
    def get_largest_cities_names(
        self, quantity: int = 100, min_population: int = 1_000_000
    ) -> list[str]:
        """Getting a list of names of the largest cities"""

        return [
            city["name"]
            for city in self.get_largest_cities_by_quantity(
                quantity=quantity,
                min_population=min_population,
            )
        ]


try:
    cities = Cities()
except Exception as init_err:
    logger.debug("Couldn't create Cities instance", exc_info=init_err)
    raise
