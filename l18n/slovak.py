# -*- coding: utf-8 -*-
from default import DefaultLocale
from dateutil.easter import easter
from datetime import date, timedelta
import calendar

class SlovakLocale(DefaultLocale):
    @property
    def month_names(self):
        return (
            "Január",
            "Február",
            "Marec",
            "Apríl",
            "Máj",
            "Jún",
            "Júl",
            "August",
            "September",
            "Október",
            "November",
            "December"
        )

    @property
    def first_day_of_week(self):
        return calendar.MONDAY   
        
    def holidays(self, year):
        hols = super(SlovakLocale, self).holidays(year)
        hols.append(date(year, 1, 1))
        hols.append(date(year, 1, 6))
        hols.append(date(year, 5, 1))
        hols.append(date(year, 5, 8))
        hols.append(date(year, 7, 5))
        hols.append(date(year, 8, 29))
        hols.append(date(year, 9, 1))
        hols.append(date(year, 9, 15))
        hols.append(date(year, 11, 1))
        hols.append(date(year, 11, 17))
        hols.append(date(year, 12, 24))
        hols.append(date(year, 12, 25))
        hols.append(date(year, 12, 26))
        
        hols.append( easter(year) + timedelta(days=-2))
        hols.append( easter(year) + timedelta(days=1))
        return hols