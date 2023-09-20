import pytest

from app.weather_picker import WeatherDataSchemeFromOpenWeather
from app.weather_picker.weather_picker import WeatherPickerWithoutSubscription, WeatherPickerWithSubscription


class TestWeatherPicker:

    @pytest.mark.parametrize(
        "weather_picker_instance_sub",
        [
            WeatherPickerWithSubscription(),
            WeatherPickerWithoutSubscription(),
        ],
    )
    @pytest.mark.asyncio
    async def test_sub_weather_picker(self, weather_picker_instance_sub, api_key):
        with_sub: bool = isinstance(weather_picker_instance_sub, WeatherPickerWithSubscription)
        weather = (
            await weather_picker_instance_sub.receive_weather_data(api_key)
            if with_sub else
            weather_picker_instance_sub.receive_weather_data(api_key)
        )
        assert weather is not None and len(weather) != 0
        for w in weather:
            assert isinstance(w, WeatherDataSchemeFromOpenWeather)
