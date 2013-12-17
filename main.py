#!/usr/bin/env python
from __future__ import division

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from locale import *

class YearCalendar(object):
    def __init__(self, year, locale=DefaultLocale()):
        self.year = year
        self.locale = locale

        # Page size and margins (overridable)
        self.pagesize = A4
        self.margins = (1*cm,) * 4   # top, right, bottom, left

        self.max_picture_height = self.content_height / 2
        self.max_table_height = self.content_height / 3

        # Register used fonts
        pdfmetrics.registerFont(TTFont("Dejavu", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejavuBold", "DejaVuSans-Bold.ttf"))

        self.title_font_name = "DejavuBold"
        self.title_bottom_margin = 0.5 * cm
        self.title_font_size = 32 #pt

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

    def render_month(self, month):
        # Render title
        title_position = (self.margins[3], self.margins[2] + self.title_bottom_margin + self.cell_height * 6)
        self.canvas.setFont(self.title_font_name, self.title_font_size)
        self.canvas.drawString(title_position[0], title_position[1], self.locale.month_title(self.year, month))

        # Render days
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
    calendar = YearCalendar(2014)
    calendar.render("calendar-2014.pdf")