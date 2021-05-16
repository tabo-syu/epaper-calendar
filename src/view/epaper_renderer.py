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

    def template(self):
        assets_dir = get_dirpath_project_root("assets")
        fonts = {
            "default": os.path.join(assets_dir, "GLT-GonunneObsolete.otf"),
            "hiragana_number": os.path.join(assets_dir, "GLT-GonunneSpurious.otf"),
        }

        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        # image = Image.open(os.path.join(assets_dir, "sample.bmp"))
        draw = ImageDraw.Draw(image)

        # title section
        date_font = ImageFont.truetype(fonts["hiragana_number"], 80)
        day_of_the_week_font = ImageFont.truetype(fonts["default"], 80)
        draw.text((25, 0), "2021.05.05", font=date_font, fill=0)
        draw.text((410, 5), "[土]", font=day_of_the_week_font, fill=0)
        draw.line((25, 110, 775, 110), fill=0, width=3)

        section_title_font = ImageFont.truetype(fonts["hiragana_number"], 56)
        # weather section
        subtitle_font = ImageFont.truetype(fonts["hiragana_number"], 32)
        weather_font = ImageFont.truetype(fonts["default"], 104)
        temperature_font = ImageFont.truetype(fonts["hiragana_number"], 24)
        draw.text((25, 107), "てんき", font=section_title_font, fill=0)
        for index in range(0, 2):
            column_spacing = 230 * index
            draw.text((28 + column_spacing, 179), "きょう", font=subtitle_font, fill=0)
            draw.text((64 + column_spacing, 221), "晴", font=weather_font, fill=0)
            draw.multiline_text(
                (30 + column_spacing, 361),
                "さいこう\nさいてい\nたいかん",
                spacing=7,
                font=temperature_font,
                fill=0,
            )
            draw.multiline_text(
                (121 + column_spacing, 361),
                "26.5ど\n19.8ど\n24.5ど",
                align="right",
                spacing=7,
                font=temperature_font,
                fill=0,
            )
            draw.line(
                (230 + column_spacing, 188, 230 + column_spacing, 456), fill=0, width=3
            )

        # plan section
        plan_date_font = ImageFont.truetype(fonts["hiragana_number"], 22)
        plan_name_font = ImageFont.truetype(fonts["default"], 32)
        draw.text((485, 107), "よてい", font=section_title_font, fill=0)
        for index in range(0, 5):
            line_spacing = 56 * index
            draw.text(
                (485, 180 + line_spacing),
                "05.16. 08.00-08.30",
                font=plan_date_font,
                fill=0,
            )
            draw.text(
                (485, 197 + line_spacing),
                "燃えるごみの日ああ",
                font=plan_name_font,
                fill=0,
            )

        return image

    def render(self):
        self.epd.init()
        self.epd.Clear()
        image = self.template()
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()
