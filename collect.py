import asyncio
import sys

from app.exceptions import FailedDownloadProjectSettings
from app.weather_picker.weather_picker import WeatherPickerWithSubscription, WeatherPickerWithoutSubscription
from app.weather_picker.weather_dao import WeatherLoaderToDatabase
from app.config import create_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = create_logger(
    logger_name="collector_logger",
    logger_level="DEBUG",
)

try:
    from app.config import settings
except ImportError as settings_err:
    logger.debug("Settings import error. Collecting stopped", exc_info=settings_err)
    raise FailedDownloadProjectSettings(exc_details=str(settings_err))


async def main():
    #  Initialize default values
    weather_picker_instance = WeatherPickerWithoutSubscription()
    checking_interval_in_hours = 1

    cmd_args = sys.argv[1:]
    for arg in cmd_args:
        if arg.startswith("--with-sub"):
            weather_picker_instance = WeatherPickerWithSubscription()
        elif arg.startswith("--interval="):
            interval = int(arg.split("=")[1])
            if not isinstance(interval, int):
                raise TypeError(f"Interval must be integer number type. Your type is {type(interval)}")
            checking_interval_in_hours = interval
    logger.debug(f"Start collecting with current flags: {cmd_args}")

    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("interval", hours=checking_interval_in_hours)
    async def collect_weather():
        logger.debug("Starting as a task")
        try:
            if isinstance(weather_picker_instance, WeatherPickerWithSubscription):
                weather = await weather_picker_instance.receive_weather_data(settings.OPENWEATHERAPI_KEY)
            else:
                weather = weather_picker_instance.receive_weather_data(settings.OPENWEATHERAPI_KEY)
            await WeatherLoaderToDatabase(weather).push_weather_to_db()
            logger.debug("Task completed ")
        except Exception as all_stop_signals:
            logger.debug("Task isn't done. Stopped...", exc_info=all_stop_signals)

    scheduler.start()
    while True:
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
