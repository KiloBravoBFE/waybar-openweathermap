Waybar weather plugin
=====================

This plugin does not use the [One Call API from OpenWeatherMap.org](https://openweathermap.org/api/one-call-3).
Instead, it uses the free API from OpenWeatherMap.org
You don't need to have an active subscription, and with normal usage you should never go over the free limit of 1000 request per day.
My refresh setting for the swaybar plugin is 300s.


## set your APIKEY and geo location in your shell

In your ~/.bashrc add the following definition and place your APIKEY in there

    # waybar weather settings:
    export WAYBAR_WEATHER_APIKEY="<YOUR OpenWeatherMap API KEY>"
    export WAYBAR_WEATHER_LAT="44.43"
    export WAYBAR_WEATHER_LON="26.02"
    export WAYBAR_WEATHER_UNITS="metric"
    export WAYBAR_WEATHER_EXCLUDE="minutely,hourly,daily"
