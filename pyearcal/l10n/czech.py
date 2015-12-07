# -*- coding: utf-8 -*-
from .default import DefaultLocale
from dateutil.easter import easter
from datetime import date, timedelta
import calendar


class CzechLocale(DefaultLocale):
    @property
    def month_names(self):
        return (
            "Leden",
            "Únor",
            "Březen",
            "Duben",
            "Květen",
            "Červen",
            "Červenec",
            "Srpen",
            "Září",
            "Říjen",
            "Listopad",
            "Prosinec"
        )

    @property
    def first_day_of_week(self):
        return calendar.MONDAY   
        
    def holidays(self, year):
        hols = super(CzechLocale, self).holidays(year)
        hols.append(date(year, 1, 1))
        hols.append(date(year, 5, 1))
        hols.append(date(year, 5, 8))
        hols.append(date(year, 7, 5))
        hols.append(date(year, 7, 6))
        hols.append(date(year, 9, 28))
        hols.append(date(year, 10, 28))
        hols.append(date(year, 11, 17))
        hols.append(date(year, 12, 24))
        hols.append(date(year, 12, 25))
        hols.append(date(year, 12, 26))

        hols.append( easter(year) + timedelta(days=1))
        if year >= 2016:
            hols.append( easter(year) + timedelta(days=-2))
        return hols
