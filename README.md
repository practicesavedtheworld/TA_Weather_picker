# TA_Weather_picker
My attempt for test assignment


## Requirements
The only things you need:

<b><i>Python</i></b> >= 3.11

<b><i>Docker</i></b> >=  24.0.6

<b><i>Docker compose</i></b> >= 2.21.0
##

## Quick run

The quick run start collecting weather for the 100 largest cities every 1 hour by default. If you want to change this behavior - check [Custom run](#custom-run)
1. Paste your API key in .test_env. Field ` OPENWEATHERAPI_KEY= `.
You can get API key after registration on https://openweathermap.org/
2. Run
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



