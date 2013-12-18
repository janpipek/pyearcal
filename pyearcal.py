#!/usr/bin/env python
from __future__ import division

from calendar import Calendar
from datetime import date

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm, inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle

from locale import *

class YearCalendar(object):
    def __init__(self, year, locale=DefaultLocale(), special_days=[]):
        self.year = year
        self.locale = locale
        self.special_days = special_days

        self.holidays = self.locale.holidays(self.year)
        self._calendar = Calendar(self.locale.first_day_of_week)

        # Page size and margins (overridable)
        self.pagesize = A4
        self.margins = (1.33*cm,) * 4   # top, right, bottom, left

        self.max_picture_height = self.content_height / 2
        self.max_table_height = self.content_height / 3

        # Register used fonts
        pdfmetrics.registerFont(TTFont("Dejavu", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejavuBold", "DejaVuSans-Bold.ttf"))

        self.title_font_name = "DejavuBold"
        self.title_bottom_margin = 1.2 * cm
        self.title_font_size = 32 #pt

        self.cell_font_name = "DejavuBold"
        self.cell_font_size = 24 #pt
        self.cell_padding = 10

        self.week_color = colors.black
        self.week_bgcolor = colors.white
        self.weekend_color = colors.white
        self.weekend_bgcolor = colors.Color(1.0, 0.7, 0.7)
        self.holiday_color = self.weekend_color
        self.holiday_bgcolor = self.weekend_bgcolor
        self.special_day_color = colors.white
        self.special_day_bgcolor = colors.blue

    @property
    def width(self):
        return self.pagesize[0]

    @property
    def height(self):
        return self.pagesize[1]

    @property
    def content_width(self):
        return self.width - self.margins[1] - self.margins[3]

    @property
    def content_height(self):
        return self.height - self.margins[0] - self.margins[2]

    @property
    def cell_height(self):
        return self.max_table_height / 6

    @property
    def cell_width(self):
        return self.content_width / 7

    def _style_holidays_and_special_days(self, month, table_style):
        calendar = self._calendar.monthdatescalendar(self.year, month)
        for row, days in enumerate(calendar):
            for column, day in enumerate(days):
                if day.month != month:
                    continue
                if day.weekday() in self.locale.weekend:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.weekend_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.weekend_color)
                if day in self.holidays:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.holiday_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.holiday_color)
                if day in self.special_days:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.special_day_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.special_day_color)

    def render_month(self, month):
        # Make a data table of days
        
        table_data = self._calendar.monthdayscalendar(self.year, month)
        table_data = [ [ day or None for day in week ] for week in table_data ]

        table = Table(table_data,
            colWidths=(self.cell_width,) * 7,
            rowHeights=(self.cell_height,) * len(table_data)
        )

        style = TableStyle()
        for padding in ("TOP", "RIGHT", "BOTTOM", "LEFT"):
            style.add(padding + "PADDING", (0, 0), (-1, -1), self.cell_padding)

        style.add("FONT", (0, 0), (-1, -1), self.cell_font_name, self.cell_font_size)
        style.add("ALIGN", (0, 0), (-1, -1), "RIGHT")
        style.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        style.add("BACKGROUND", (0, 0), (-1, -1), self.week_bgcolor)
        # style.add("BACKGROUND", (5, 0), (-1, -1), self.weekend_bgcolor)
        style.add("TEXTCOLOR", (0, 0), (-1, -1), self.week_color)
        # style.add("TEXTCOLOR", (5, 0), (-1, -1), self.weekend_color)
        self._style_holidays_and_special_days(month, style)

        table.setStyle(style)



        table_width, table_height = table.wrapOn(self.canvas, 7*self.cell_width, 6*self.cell_height)
        table.drawOn(self.canvas, self.margins[3], self.margins[2])
        
        # Render title
        title_position = (self.margins[3], self.margins[2] + table_height + self.title_bottom_margin)
        self.canvas.setFont(self.title_font_name, self.title_font_size)
        self.canvas.drawString(title_position[0], title_position[1], self.locale.month_title(self.year, month))

        self.canvas.showPage()

    def render_title_page(self):
        self.canvas.showPage()

    def render(self, file_name):
        self.canvas = canvas.Canvas(file_name, self.pagesize)
        self.render_title_page()
        for month in xrange(1, 13):
            self.render_month(month)
        self.canvas.save()

if __name__ == "__main__":
    cal = YearCalendar(2014, CzechLocale(), special_days=[ date(2014, 11, 11) ])
    print cal.locale.first_day_of_week
    cal.render("calendar-2014.pdf")