#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os

import requests

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(env_path)
from env import OWM_API_KEY


class OpenWeatherMap:
    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/onecall"

    def get_daily_forecast(self, input_payload):
        payload = {
            "units": "metric",
            "appid": OWM_API_KEY,
            "exclude": "current,minutely,hourly,alerts",
        }
        payload.update(input_payload)
        daily_forecast = requests.get(self.url, params=payload).json()["daily"]

        for index, day in enumerate(daily_forecast):
            daily_forecast[index]["weather"][0]["icon"] = self.get_primary_weather(
                day["weather"][0]["icon"]
            )

        return daily_forecast

    def get_primary_weather(self, icon_id):
        # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
        weather_list = {
            "01d": "快晴",
            "01n": "快晴",
            "02d": "晴",
            "02n": "晴",
            "03d": "雲",
            "03n": "雲",
            "04d": "雲",
            "04n": "雲",
            "09d": "小雨",
            "09n": "小雨",
            "10d": "雨",
            "10n": "雨",
            "11d": "雷",
            "11n": "雷",
            "13d": "雪",
            "13n": "雪",
            "50d": "霧",
            "50n": "霧",
        }

        return weather_list[icon_id]
