from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, exists

from app.config import session
from app.weather_picker import WeatherDataSchemeFromOpenWeather, CityModelScheme, CityTimestampScheme, \
    MainWeatherScheme, ExtraWeatherScheme
from app.weather_picker.models import CityModel, CityTimestamp, MainWeather, ExtraWeather


#  TODO handler, docstring, crud logic

class CityDataMapper(ABC):

    @staticmethod
    @abstractmethod
    def map_city(weather_data: WeatherDataSchemeFromOpenWeather) -> CityModelScheme:
        ...

    @staticmethod
    @abstractmethod
    def map_timestamp(city_id: int) -> CityTimestampScheme:
        ...

    @staticmethod
    @abstractmethod
    def map_main_weather(weather_data: WeatherDataSchemeFromOpenWeather) -> tuple[
        MainWeatherScheme,
        WeatherDataSchemeFromOpenWeather,
    ]:
        ...

    @staticmethod
    @abstractmethod
    def map_extra_weather(weather_data: WeatherDataSchemeFromOpenWeather, city_id: int) -> ExtraWeatherScheme:
        ...


class CityDataMapperImpl(CityDataMapper):

    @staticmethod
    def map_city(weather_data: WeatherDataSchemeFromOpenWeather) -> CityModelScheme:
        """ """

        name = weather_data["name"]
        city_coordinates: dict[str, float] = weather_data["coord"]
        longitude, latitude = city_coordinates.get("lon", 0.), city_coordinates.get("lat", 0.)
        county = weather_data["sys"].get("country")

        return CityModelScheme(
            **dict(
                name=name,
                latitude=latitude,
                longitude=longitude,
                county=county,
            ))

    @staticmethod
    def map_timestamp(city_id: int) -> CityTimestampScheme:
        current_utc_time = datetime.utcnow()
        return CityTimestampScheme(
            **dict(
                city_id=city_id,
                created_at=current_utc_time,
                updated_at=current_utc_time,
            )
        )

    @staticmethod
    def map_main_weather(
            weather_data: WeatherDataSchemeFromOpenWeather,
    ) -> tuple[
        MainWeatherScheme,
        WeatherDataSchemeFromOpenWeather,
    ]:
        """ """

        return MainWeatherScheme(
            **weather_data.get("main")
        ), weather_data

    @staticmethod
    def map_extra_weather(weather_data: WeatherDataSchemeFromOpenWeather, city_id: int) -> ExtraWeatherScheme:
        """ """

        return ExtraWeatherScheme(
            **dict(
                city_id=city_id,
                visibility=weather_data.visibility,
                wind=weather_data.wind,
                recorded_at=datetime.utcnow(),
            ))


@dataclass
class BaseWeatherDatabase:
    weather: list[WeatherDataSchemeFromOpenWeather]
    client_session: AsyncSession = session
    weather_data: list[
                      tuple[
                          CityModelScheme,
                          tuple[
                              MainWeatherScheme,
                              WeatherDataSchemeFromOpenWeather,
                          ],
                      ],
                  ] | None = None
    city_data_mapper = CityDataMapperImpl()

    def __post_init__(self) -> None:
        self.weather_data = self.gain_viable_weather_data()

    def gain_viable_weather_data(self) -> list[
        tuple[
            CityModelScheme,
            tuple[
                MainWeatherScheme,
                WeatherDataSchemeFromOpenWeather,
            ],
        ]
    ]:
        """ """

        weather_data = []
        for weather in self.weather:
            city = self.city_data_mapper.map_city(weather)
            main_weather = self.city_data_mapper.map_main_weather(weather)
            weather_data.append((city, main_weather))

        return weather_data


##########################################
##          Insert Operations           ##
##########################################


class WeatherLoaderToDatabase:
    def __init__(self, weather: list[WeatherDataSchemeFromOpenWeather], client_session: AsyncSession) -> None:
        self.base_weather: BaseWeatherDatabase = BaseWeatherDatabase(
            weather=weather,
            client_session=client_session,
        )
        self.weather_data = self.base_weather.weather_data
        self.data_mapper_link = self.base_weather.city_data_mapper

    async def push_weather_to_db(self):
        """ """

        async with self.base_weather.client_session as push_session:
            for city, main_weather in self.weather_data:
                try:
                    await push_session.begin()
                    #  Begin Transaction

                    is_city_exist_in_citymodel = exists().where(city["name"] == CityModel.name)
                    if not is_city_exist_in_citymodel:
                        #  CityModel
                        push_city_ret_id_query = (
                            insert(CityModel)
                            .values(**city)
                            .returning(CityModel.id)
                        )
                        push_city_ret_id_query_result = await push_session.execute(push_city_ret_id_query)
                        city_id = push_city_ret_id_query_result.scalar()
                        is_city_exist_in_citytimestamp = exists().where(CityTimestamp.city_id == city_id)

                        if not is_city_exist_in_citytimestamp:
                            #  CityTimestamp
                            city_timestamp = self.data_mapper_link.map_timestamp(city_id=city_id)
                            push_city_timestamp_query = (
                                insert(CityTimestamp)
                                .values(**city_timestamp)
                            )
                            await push_session.execute(push_city_timestamp_query)

                        #  MainWeather
                        push_mainweather_query = (
                            insert(MainWeather)
                            .values(city_id=city_id, **main_weather[0])

                        )
                        await push_session.execute(push_mainweather_query)

                        #  ExtraWeather
                        extra_weather = self.data_mapper_link.map_extra_weather(
                            weather_data=main_weather[1],
                            city_id=city_id,
                        )
                        push_extraweather_query = (
                            insert(ExtraWeather)
                            .values(**extra_weather)
                        )
                        await push_session.execute(push_extraweather_query)
                    await push_session.commit()
                    # End of Transaction
                except:
                    #  TODO handle this
                    ...
