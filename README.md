
# TA_Weather_picker
My attempt for test assignment
##

## Conditions of the problem
<details>
  <summary>  :pencil2: TEST ASSIGNMENT </summary>
<details>
  <summary>  EN </summary>
   Exercise:
The business challenge sounds like this:
"We need to have weather data in the 100 largest cities in the world, based on this data we will manage the capacity of Data Centers in terms of cooling and load"

Clarification of the task from the lead:
"Write a Collector (an entity responsible for collecting statistics) for https://openweathermap.org/, which should each collect weather information for the 100 largest cities in the world, and then save the value in the database. When collecting, pay attention to side data, which can be obtained, can we use them for something? When writing, keep in mind that the code may change frequently, so you should think about expanding it and further supporting it. The choice of technologies is at your discretion."


Optional:
-Describe why this database structure was chosen?
-Why was this or that technology chosen?
-What technological limitations are there at this stage?

The repository should have a readme file that contains documentation and startup instructions.

Necessarily:
When you initially configure and launch the composition, the collector will begin to work and collect data.

The result should be posted on Github, the link to which will be sent to my telegram.
Good luck
</details>
<details>
  <summary>  RU </summary>
   Задание:
Задача от бизнеса звучит так:
"Нам нужно иметь данные о погоде в 100 крупнейших городах мира, на основании этих данных мы будем управлять мощностями Дата-центров в плане охлаждения и нагрузки "

Уточнение задачи от лида:
"Напиши Коллектор (сущность, отвечающую за сбор и статистики) для https://openweathermap.org/, который должен каждый собирать информацию о погоде для 100 крупнейших городов мира, после чего сохранять значение в БД. При сборе обрати внимание на побочные данные, которые можно получить, можем ли мы их для чего-то использовать? При написании следует учитывать, что код может часто меняться, поэтому следует подумать о его расширении и дальнейшей поддержке. Выбор технологий на твое усмотрение."


Опционально:
-Описать почему выбрана такая структура БД?
-Почему выбрана та или иная технология?
-Какие технологические ограничения есть на данном этапе?

В репозитории должен быть файл readme, в котором содержится документация и инструкция по запуску.

Обязательно:
При первоначальной настройке и запуске компоуза коллектор начнет работать и собирать даннные.

Результат должен быть размещен на гитхабе, ссылка на который скинута в мой телеграм.
Удачи
</details>
</details>

##

## Technologies


![](https://img.shields.io/badge/python/3.10.4?color=blue)

![](https://img.shields.io/badge/python-3.11-blue)
![](https://img.shields.io/badge/SQLAlchemy-2.0.20-orange)
![](https://img.shields.io/badge/aiohttp-3.8.5-blue)
![](https://img.shields.io/badge/alembic-1.12.0-orange)
![](https://img.shields.io/badge/pydantic-2.3.0-orange)
![](https://img.shields.io/badge/requests-2.31.0-blue)
![](https://img.shields.io/badge/APScheduler-3.10.4-orange)

##

![](https://img.shields.io/badge/black-23.9.1-blue)
![](https://img.shields.io/badge/flake8-6.1.0-blue)
![](https://img.shields.io/badge/isort-5.12.0-blue)

## What is Weather picker
![weather](https://github.com/practicesavedtheworld/TA_Weather_picker/assets/105741091/6c17a725-4934-4da8-b01d-09d34156a15e)

Wheather picker is a programm that collect weather for 100 largest cities using OpenWeather API
Application has 2 different way of collection:
 - With subscription (using aiohttp library)
 - No sub (usinb request library)

The main diffence between them is collecting speed.

&#9888; Note that this educational project and sub mode is ebanle by just added `--with-sub` flag.

Weather data is entered into a database. The database looks like
![Database](https://github.com/practicesavedtheworld/TA_Weather_picker/assets/105741091/d10d2daa-e203-4017-93a7-65975fd1000f)

This scheme allows to organize the storage of data about cities, weather and provide relations between them.

I chose PostgreSQL because it is a powerful database server that can efficiently handle large amounts of data and support multiple clients. This allows the database to scale as the number of cities and weather data grows. PostgreSQL also offers query optimization, indexes, and other mechanisms that help improve performance.

Since my application has a artificial subscription, I used `requests` and `aiohttp` libraries to get the weather information.

Aiohttp is asynchronous, so I used this for collector with subscription.

The `WeatherPickerWithSubscription` class is an implementation of `WeatherPicker` using the `aiohttp` library to retrieve weather data asynchronously.

The `WeatherPickerWithoutSubscription` class represents an implementation of `WeatherPicker` using the `requests` library to retrieve weather data.

For getting the largest cities I used <a href='https://github.com/yaph/geonamescache'>geonamescache</a> library. Geonames data is obtained from [GeoNames](http://www.geonames.org/).

The entire program runs in Docker. When you run the collector, it starts the database service and tries to pass all the tests. If everything is ok, then you may see something like this in the program log:



![Снимок экрана от 2023-09-21 22-20-47](https://github.com/practicesavedtheworld/TA_Weather_picker/assets/105741091/7bacc9dd-620f-4e18-a7b3-cf4ac2a3b0dc)


##

## Requirements
The only things you need:

<b><i>Python</i></b> >= 3.11

<b><i>Docker</i></b> >=  24.0.6

<b><i>Docker compose</i></b> >= 2.21.0
##

## Quick run

The quick run start collecting weather for the 100 largest cities every 1 hour by default. If you want to change this behavior - check [Custom run](#custom-run)
1. ```sh
   git clone https://github.com/practicesavedtheworld/TA_Weather_picker
   ```
2. ```sh
   cd TA_Weather_picker
   pip install requirements.txt
   ```

3. Paste your API key in .test_env. Field ` OPENWEATHERAPI_KEY= `.
You can get API key after registration on https://openweathermap.org/

&#9888; Note: Without OpenWeather API Key it won't work

4. Run
```sh
   docker compose up --build
```

##

## Custom run

Weather picker maintain 2 flags.

|  FLAG | TASK |
| ----------- | ----------- |
| --with-sub    | Tells application that collecting will be asynchronously way. Default is no sub instance runs   |
| --interval    | How often to get the actual weather in hours. Default is 1 hour   |

So, you can change, for example interval.
Just change the value in `collect.sh` file


<code><b>python3 collect.py --with-sub --interval=24</b></code>

Now it's collect weather every 24 hours.

&#9888; Note that script must running on background
##

## Run as a python script


1. ```sh
   git clone https://github.com/practicesavedtheworld/TA_Weather_picker
   ```
2. ```sh
   cd TA_Weather_picker
   pip install requirements.txt
   ```

3. Paste your API key in .test_env. Field ` OPENWEATHERAPI_KEY= `.
You can get API key after registration on https://openweathermap.org/

&#9888; Note: Without OpenWeather API Key it won't work

4. Run
```sh
   python3 collect.py --with-sub --interval=1
```


