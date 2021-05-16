#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime
import locale
import logging

from model.google_calendar import GoogleCalendar
from model.open_weather_map import OpenWeatherMap
from view.epaper_renderer import EpaperRenderer


def main():
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

    now = datetime.now()
    date_str = now.strftime("%Y.%m.%d")
    day_of_week_str = now.strftime("%a")

    weather = OpenWeatherMap()
    daily_forcast = weather.get_daily_forecast({"lat": "35.71", "lon": "139.81"})

    calendar = GoogleCalendar()
    events = []
    for event in calendar.get_events(calendar_id="primary", max_results=5):
        events.append(
            {
                "period": event["period"],
                "summary": event["summary"],
            }
        )

    renderer = EpaperRenderer()
    renderer.render(
        {
            "date": date_str,
            "day_of_week": day_of_week_str,
            "forecasts": [daily_forcast[0], daily_forcast[1]],
            "events": events,
        }
    )


try:
    main()

except IOError as e:
    logging.info(e)
