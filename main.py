#!/usr/bin/env python
# import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class YearCalendar(object):
    def __init__(self, year):
        self.year = year
        self.pagesize = A4

    def render_month(self, month):
        self.canvas.showPage()

    def render(self, file_name):
        self.canvas = canvas.Canvas(file_name, self.pagesize)
        for month in xrange(1, 13):
            self.render_month(month)
        self.canvas.save()

if __name__ == "__main__":
    calendar = YearCalendar(2014)
    calendar.render("calendar-2014.pdf")