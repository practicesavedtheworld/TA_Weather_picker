import asyncio
from pprint import pprint

import aiohttp

from app import WeatherDataSchemeFromOpenWeather


async def main() -> WeatherDataSchemeFromOpenWeather:
    async with aiohttp.ClientSession() as session:
        url = "https://api.openweathermap.org/data/2.5/weather?q=delhi&appid=eb6ce92e849aaa6fd4d4f7c98960a0a6"
        response = await session.get(url)
        data = await response.json()
        # import requests
        # r = requests.get(url)
        #
        # pprint(data)
        # print()
        # pprint(r.json())
        s = WeatherDataSchemeFromOpenWeather(**data)
        pprint(s.model_dump())
        return s
        # Обработка данных погоды
        # weather_list = data['list']
        # for weather in weather_list:
        #     timestamp = weather['dt']
        #     temperature = weather['main']['temp']
        #     description = weather['weather'][0]['description']
        #     print(f"Timestamp: {timestamp}, Temperature: {temperature}, Description: {description}")

if __name__ == '__main__':
    _url = "https://api.openweathermap.org/data/2.5/weather?q={x}&appid={r}"
    print(_url.format(x = 123, r = 1111))
    # asyncio.run(main())