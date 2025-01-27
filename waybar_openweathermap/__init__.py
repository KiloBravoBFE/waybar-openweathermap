#!/usr/bin/env python3

import json
import requests
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import time

ICON_MAP = {
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧️",
    "10d": "🌦️",
    "11d": "⛈️",
    "13d": "🌨️",
    "50d": "🌫",
}

UNITS_MAP = {
    "standard": ("K", "m/sec"),
    "metric": ("°C","m/sec"),
    "imperial": ("°F", "mph"),
    "metric-simple": ("°", "m/s"),
}

COMPASS_POINTS = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW', 'N']
def deg_to_dir(deg):
    deg = deg%360
    for i in range(len(COMPASS_POINTS)):
        d = i*22.5
        if d-11.25 <= deg and deg < d+11.25:
           return COMPASS_POINTS[i]

    return 'Uknown'

def main():

    try:
        ip = requests.get("https://ipinfo.io/ip").text
        try:
            postal = int(requests.get(f"https://ipinfo.io/{ip}/postal").text)
        except Exception as e:
            return print({})
    except Exception as e:
        return print({})

    # Handle wrong / useless postal codes
    bielefeld = {33607, 33609, 33611, 33613, 33615, 33617, 33519}
    if (postal in bielefeld):
        postal = 33619
    # Handle Telefónica NRW IP-range (useless)
    elif (ip.startswith("176.1.")):
        postal = default_postal
    
    dst_active = time.localtime().tm_isdst
    tz = time.tzname[dst_active]

    apikey = os.getenv("WAYBAR_WEATHER_APIKEY")
    default_postal = os.getenv("WAYBAR_WEATHER_DEF_POSTAL", 33619)
    units = os.getenv("WAYBAR_WEATHER_UNITS", "metric")
    icon_units = os.getenv("WAYBAR_WEATHER_ICON_UNITS", "metric-simple")

    if (not postal):
        postal = default_postal
    
    data = {}
    try:
        url = (f"https://api.openweathermap.org/data/2.5/weather?zip={postal},de&appid={apikey}&units={units}")
        weather = requests.get(url).json()

    except Exception as e:
        return print({})

    # Handles error codes
    if weather.get("cod"):
        data["text"] = "[weather] Error {}: {}".format(
            weather.get("cod"), weather.get("message")
        )
        try:
            assert data["text"][16:19] == "200"
        except AssertionError:
            data["class"] = "weather"
            print(json.dumps(data))
            sys.exit(data["text"])
            sys.exit()


    temp = weather["main"]["temp"]
    icon = ICON_MAP.get(weather["weather"][0]["icon"], "")
    feels_like = weather["main"]["feels_like"]
    humidity = weather["main"]["humidity"]
    pressure = weather["main"]["pressure"]
    sunrise = datetime.fromtimestamp(
        weather["sys"]["sunrise"], ZoneInfo(tz)
    ).strftime("%H:%M")
    sunset = datetime.fromtimestamp(
        weather["sys"]["sunset"], ZoneInfo(tz)
    ).strftime("%H:%M")
    wind_speed = weather["wind"]["speed"]
    wind_direction = deg_to_dir(weather["wind"]["deg"])
    uvi = weather["sys"]["type"] #TODO
    city = weather["name"]
    country_code = weather["sys"]["country"]

    data["text"] = f"{icon} {temp:.1f}{UNITS_MAP[icon_units][0]}"
    data["tooltip"] = f"""
        City: {city}, {postal}, {country_code}
        Feels like: {feels_like:.1f}{UNITS_MAP[units][0]}
        Pressure: {pressure} hPa
        Humidity: {humidity}%
        UV Index: {uvi}
        Sunrise: {sunrise}
        Sunset: {sunset}
        Wind: {wind_direction}, {wind_speed:.0f} {UNITS_MAP[units][1]}"""
    if "daily" in weather:
        temp_min = weather["daily"][0]["temp"]["min"]
        temp_max = weather["daily"][0]["temp"]["max"]
        data["tooltip"] = f"""Min: {temp_min:.1f}{UNITS_MAP[units][0]}
Max: {temp_max:.1f}{UNITS_MAP[units][0]}
""" + data["tooltip"]

    data["class"] = "weather"

    print(json.dumps(data))


if __name__ == "__main__":
    main()
