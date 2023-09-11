from abc import ABC, abstractmethod

import aiohttp

from app import WeatherDataSchemeFromOpenWeather, create_logger

logger = create_logger("weather_picker_logger", logger_level="INFO")


class WeatherPicker(ABC):

    @abstractmethod
    def receive_weather_data(self, city_name: str, api_key: str) -> WeatherDataSchemeFromOpenWeather:
        ...


class WeatherPickerWithSubscription(WeatherPicker):

    async def receive_weather_data(self, city_name: str, api_key: str) -> WeatherDataSchemeFromOpenWeather:
        """Note that subscription gives asynchronous weather collecting, so it's faster"""

        async with aiohttp.ClientSession() as session:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        weather_data = await response.json()
                        return WeatherDataSchemeFromOpenWeather(**weather_data)
                    else:
                        # TODO add custom exp
                        logger.warning(f"API is alive, but request[{url}] had failed.")
            except aiohttp.ClientError as c_err:
                #  TODO add custom exp
                logger.critical(f"Some error occur while picking weather. \nDetails: {c_err}")


class WeatherPickerWithoutSubscription(WeatherPicker):

    def receive_weather_data(self, city_name: str, api_key: str) -> WeatherDataSchemeFromOpenWeather:
        ...
