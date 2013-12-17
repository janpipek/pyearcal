#!/usr/bin/env python
# import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm, inch

from locale import *

class YearCalendar(object):
    def __init__(self, year, locale=DefaultLocale()):
        self.year = year
        self.locale = locale

        self.pagesize = A4
        self.width, self.height = self.pagesize
        self.margins = (1*cm,) * 4   # top, right, bottom, left
        self.content_width = self.width - self.margins[1] - self.margins[3]
        self.content_height = self.height - self.margins[0] - self.margins[2]

    def render_month(self, month):
        position = (1*cm, 12*cm)
        self.canvas.drawString(position[0], position[1], self.locale.month_title(self.year, month))
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