#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

from PIL import Image, ImageDraw, ImageFont


def get_dirpath_project_root(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        name,
    )


lib_dir = get_dirpath_project_root("lib")
sys.path.append(lib_dir)
from waveshare_epd.epd7in5_V2 import EPD


class EpaperRenderer:
    def __init__(self):
        self.epd = EPD()

    def template(self, data):
        assets_dir = get_dirpath_project_root("assets")
        fonts = {
            "default": os.path.join(assets_dir, "GLT-GonunneObsolete.otf"),
            "hiragana_number": os.path.join(assets_dir, "GLT-GonunneSpurious.otf"),
        }

        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)

        # title section
        date_font = ImageFont.truetype(fonts["hiragana_number"], 80)
        day_of_the_week_font = ImageFont.truetype(fonts["default"], 80)
        draw.text((25, 0), data["date"], font=date_font, fill=0)
        draw.text(
            (410, 5), f'[{data["day_of_week"]}]', font=day_of_the_week_font, fill=0
        )
        draw.line((25, 110, 775, 110), fill=0, width=3)

        section_title_font = ImageFont.truetype(fonts["hiragana_number"], 56)
        # weather section
        subtitle_font = ImageFont.truetype(fonts["hiragana_number"], 32)
        weather_font = ImageFont.truetype(fonts["default"], 104)
        temperature_font = ImageFont.truetype(fonts["hiragana_number"], 24)
        draw.text((25, 107), "てんき", font=section_title_font, fill=0)
        for index, forecast in enumerate(data["forecasts"]):
            column_spacing = 230 * index
            draw.text(
                (28 + column_spacing, 179),
                "きょう" if index == 0 else "あした",
                font=subtitle_font,
                fill=0,
            )
            draw.text(
                (116 + column_spacing, 219),
                forecast["weather"][0]["icon"],
                font=weather_font,
                fill=0,
                align="center",
                anchor="ma",
            )
            draw.multiline_text(
                (28 + column_spacing, 361),
                "さいこう\nさいてい\nたいかん",
                spacing=7,
                font=temperature_font,
                fill=0,
            )
            draw.multiline_text(
                (206 + column_spacing, 361),
                f'{forecast["temp"]["max"]}ど\n{forecast["temp"]["min"]}ど\n{forecast["feels_like"]["day"]}ど',
                spacing=7,
                font=temperature_font,
                fill=0,
                align="right",
                anchor="ra",
            )
            draw.line(
                (230 + column_spacing, 188, 230 + column_spacing, 456), fill=0, width=3
            )

        # plan section
        plan_date_font = ImageFont.truetype(fonts["hiragana_number"], 22)
        plan_name_font = ImageFont.truetype(fonts["default"], 32)
        draw.text((485, 107), "よてい", font=section_title_font, fill=0)
        for index, event in enumerate(data["events"]):
            line_spacing = 56 * index
            draw.text(
                (485, 180 + line_spacing),
                event["period"],
                font=plan_date_font,
                fill=0,
            )
            draw.text(
                (485, 197 + line_spacing),
                event["summary"],
                font=plan_name_font,
                fill=0,
            )

        return image

    def render(self, data):
        self.epd.init()
        self.epd.Clear()
        image = self.template(data)
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()
