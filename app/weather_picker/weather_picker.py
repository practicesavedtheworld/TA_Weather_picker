import asyncio
import functools
from abc import ABC, abstractmethod

from aiohttp import ClientError, ClientSession
from requests import get, ConnectionError, HTTPError

from app.cities import cities
from app.config import create_logger
from app.weather_picker import WeatherDataSchemeFromOpenWeather

logger = create_logger("weather_picker_logger", logger_level="INFO")


class WeatherPicker(ABC):
    _url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    @abstractmethod
    def receive_weather_data(self, api_key: str) -> list[WeatherDataSchemeFromOpenWeather]:
        ...


class WeatherPickerWithSubscription(WeatherPicker):
    """Using aiohttp library"""

    def __init__(self):
        self._session = ClientSession()

    @staticmethod
    async def fetch_weather(aio_session, current_url) -> WeatherDataSchemeFromOpenWeather:
        async with aio_session.get(current_url) as response:
            if response.status == 200:
                weather = await response.json()
                return WeatherDataSchemeFromOpenWeather(**weather)
            else:
                logger.warning(f"API is alive, but request[{current_url}] had failed.")

    @functools.lru_cache(maxsize=50)
    async def receive_weather_data(self, api_key: str) -> list[WeatherDataSchemeFromOpenWeather]:
        """Note that subscription gives asynchronous weather collecting, so it's faster"""

        # weather_data contains the only successful responses from openweather
        # Failed response does not push into weather_data
        weather_data: list[WeatherDataSchemeFromOpenWeather] = []
        async with self._session:
            try:
                tasks = []
                for city in cities.get_largest_cities_names():
                    url = self._url.format(city_name=city, api_key=api_key)
                    tasks.append(asyncio.create_task(self.fetch_weather(self._session, url)))
                responses = await asyncio.gather(*tasks)  # type ignore

                for response in responses:
                    response: WeatherDataSchemeFromOpenWeather
                    if response is not None:
                        weather_data.append(response)
                return weather_data
            except ClientError as client_err:
                # TODO: add custom exception handling
                logger.critical(f"Some error occurred while picking weather. \nDetails: {client_err}")


class WeatherPickerWithoutSubscription(WeatherPicker):
    """Using request library"""

    @functools.lru_cache(maxsize=50)
    def receive_weather_data(self, api_key: str) -> list[WeatherDataSchemeFromOpenWeather]:
        """Default weather picker version. Slow but free"""

        # weather_data contains the only successful responses from openweather
        # Failed response does not push into weather_data
        weather_data = []
        try:
            for city in cities.get_largest_cities_names():
                url = self._url.format(city_name=city, api_key=api_key)
                response = get(url)
                if response.status_code == 200:
                    weather = WeatherDataSchemeFromOpenWeather(**response.json())
                    weather_data.append(weather)
            return weather_data
        except (HTTPError, ConnectionError) as req_err:
            # TODO: add custom exception handling
            logger.error(f"Connection refused or there is some HTTP error: {req_err}")
