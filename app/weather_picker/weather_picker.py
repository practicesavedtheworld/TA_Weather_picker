from abc import ABC, abstractmethod


class WeatherPicker(ABC):

    @abstractmethod
    def receive_weather_data(self):
        ...


class WeatherPickerWithSubscription(WeatherPicker):

    async def receive_weather_data(self):
        ...


class WeatherPickerWithoutSubscription(WeatherPicker):

    def receive_weather_data(self):
        ...
