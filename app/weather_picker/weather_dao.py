from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, exists, select, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, OperationalError

from app.config import session, create_logger
from app.weather_picker import WeatherDataSchemeFromOpenWeather, CityModelScheme, CityTimestampScheme, \
    MainWeatherScheme, ExtraWeatherScheme
from app.weather_picker.models import CityModel, CityTimestamp, MainWeather, ExtraWeather

logger = create_logger(
    logger_name="database_logger",
    logger_level="DEBUG"
)


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
    def map_main_weather(
            weather_data: WeatherDataSchemeFromOpenWeather
    ) -> tuple[
        MainWeatherScheme,
        WeatherDataSchemeFromOpenWeather,
    ]:
        ...

    @staticmethod
    @abstractmethod
    def map_extra_weather(
            weather_data: WeatherDataSchemeFromOpenWeather,
            city_id: int,
    ) -> ExtraWeatherScheme:
        ...


class CityDataMapperImpl(CityDataMapper):

    @staticmethod
    def map_city(weather_data: WeatherDataSchemeFromOpenWeather) -> CityModelScheme:
        """Create city scheme and validate fields with pydantic. """

        name = weather_data.name
        city_coordinates: dict[str, float] = weather_data.coord.model_dump()
        longitude, latitude = city_coordinates.get("lon", 0.), city_coordinates.get("lat", 0.)
        country = weather_data.sys.get("country")

        return CityModelScheme(
            **dict(
                name=name,
                latitude=latitude,
                longitude=longitude,
                country=country,
            ))

    @staticmethod
    def map_timestamp(city_id: int) -> CityTimestampScheme:
        """Add timestamp for current city, for tracking changes."""
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
        """Create main weather scheme and validate fields with pydantic. """

        return weather_data.model_dump().get("main"), weather_data

    @staticmethod
    def map_extra_weather(weather_data: WeatherDataSchemeFromOpenWeather, city_id: int) -> ExtraWeatherScheme:
        """Create extra weather scheme and validate fields with pydantic."""

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
        """Viable means that only few fields from openweatherapi will include in return value."""

        weather_data = []
        for weather in self.weather:
            city = self.city_data_mapper.map_city(weather)
            main_weather = self.city_data_mapper.map_main_weather(weather)
            weather_data.append((city, main_weather))
        else:
            logger.info("Successfully gain viable weather data")
        return weather_data


class CRUDWeatherDAO:
    """Base class for CRUD operations"""

    def __init__(self, weather: list[WeatherDataSchemeFromOpenWeather]) -> None:
        self.base_weather: BaseWeatherDatabase = BaseWeatherDatabase(
            weather=weather,

        )
        self.weather_data = self.base_weather.weather_data
        self.data_mapper_link = self.base_weather.city_data_mapper


###################################################
##          Insert / Update Operations           ##
###################################################

class WeatherLoaderToDatabase(CRUDWeatherDAO):

    async def push_weather_to_db(self) -> None:
        """Add weather to database.

         Does these steps as transaction for each city in list of cities:
         1) Identify city(gets id). If city doesn't exist create it
         2) Note city timestamp
         3) Add main weather for current city
         4) Add extra weather for current city"""

        async with self.base_weather.client_session as push_session:
            try:
                for city, main_weather in self.weather_data:
                    try:
                        #  Begin Transaction
                        async with push_session.begin():
                            city_id = await self.get_or_create_city(push_session, city)
                            await self.update_city_timestamp(push_session, city_id)
                            await self.push_main_weather(push_session, city_id, main_weather[0])
                            await self.push_extra_weather(push_session, city_id, main_weather[1])
                        #  End Transaction
                    except OperationalError as db_conn_err:
                        logger.debug("Can't connect to database", exc_info=db_conn_err)
                        raise
                    except DBAPIError as db_err:
                        logger.debug("The execution of a database operation fails", exc_info=db_err)
                        raise
                    except SQLAlchemyError as tran_err:
                        logger.debug(f"Problem occur with city {city} and weather{main_weather}."
                                     f"Skip this city...", exc_info=tran_err)
                        raise
            except KeyboardInterrupt:
                logger.debug("STOPPED MANUALLY")
                raise
            except Exception as err:
                logger.debug("Cant handle city's weather", exc_info=err)
                raise

    async def get_or_create_city(self, push_session: AsyncSession, city: CityModelScheme) -> int:
        try:
            existing_city = await push_session.execute(select(CityModel.id).where(CityModel.name == city.name))
            city_id = existing_city.scalar_one_or_none()
            if city_id is None:
                city_id = await self.create_city(push_session, city)
            return city_id
        except (SQLAlchemyError, ValidationError) as err:
            logger.debug("Failed attempt to create city or scheme isn't relevant to db model", exc_info=err)
            raise

    async def create_city(self, push_session: AsyncSession, city) -> int:
        try:
            city_query = insert(CityModel).values(**city.model_dump()).returning(CityModel.id)
            city_query_result = await push_session.execute(city_query)
            city_id = city_query_result.scalar()
            city_timestamp = self.data_mapper_link.map_timestamp(city_id=city_id)
            await push_session.execute(insert(CityTimestamp).values(**city_timestamp.model_dump()))
            return city_id
        except ValidationError as v_err:
            logger.debug("Scheme isn't relevant to db model", exc_info=v_err)
        except SQLAlchemyError as db_err:
            logger.debug(f"City {city} wasn't create", exc_info=db_err)

    @staticmethod
    async def update_city_timestamp(
            push_session: AsyncSession,
            city_id: int,
    ) -> None:
        try:
            city_timestamp_query = (
                update(CityTimestamp)
                .where(CityTimestamp.city_id == city_id)
                .values(
                    updated_at=datetime.utcnow(),
                )
            )
            await push_session.execute(city_timestamp_query)
        except SQLAlchemyError as err:
            logger.debug("Failed to update city timestamp", exc_info=err)
            raise

    @staticmethod
    async def push_main_weather(
            push_session: AsyncSession,
            city_id: int,
            main_weather: dict,
    ) -> None:
        try:
            weather_exist = await push_session.execute(select(MainWeather).where(MainWeather.city_id == city_id))

            if not weather_exist.scalar_one_or_none():
                main_weather_query = (
                    insert(MainWeather)
                    .values(city_id=city_id, **main_weather)
                )
            else:
                main_weather_query = (
                    update(MainWeather)
                    .where(MainWeather.city_id == city_id)
                    .values(**main_weather)
                )
            await push_session.execute(main_weather_query)
        except SQLAlchemyError as err:
            logger.debug("Failed to push main weather data", exc_info=err)
            raise

    async def push_extra_weather(
            self,
            push_session: AsyncSession,
            city_id: int,
            extra_weather: WeatherDataSchemeFromOpenWeather,
    ) -> None:
        try:
            extra_weather_viable = self.data_mapper_link.map_extra_weather(extra_weather, city_id=city_id)
            extra_weather_query = (
                insert(ExtraWeather)
                .values(**extra_weather_viable.model_dump())
            )
            await push_session.execute(extra_weather_query)
        except SQLAlchemyError as err:
            logger.debug("Failed to push extra weather data", exc_info=err)
            raise


###################################################
##               Delete Operations               ##
###################################################


class WeatherDeleterFromDatabase(CRUDWeatherDAO):
    ...


###################################################
##               Read Operations                 ##
###################################################

class WeatherReaderFromDatabase(CRUDWeatherDAO):
    ...
