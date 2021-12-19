# -*- coding: utf-8 -*-
from .default import DefaultLocale
from dateutil.easter import easter
from datetime import date, timedelta
import calendar


class ItalianLocale(DefaultLocale):
    """Italian variant of the calendar.

    Includes holiday both national and local. Specify
    province or city (by its Italian name) in the constructor
    if needed.

    Local holidays are included for the following:

    **Cities:** Bari, Bologna, Cagliari, Firenze, Genova, Milano,
       Napoli, Palermo, Roma, Torino, Trieste
    **Provinces:** Bolzano (Alto Adige)
    """

    def __init__(self, city=None, province=None):
        """
        :type province: str
        """
        super(ItalianLocale, self).__init__()
        if city:
            self.city = city.lower()
        else:
            self.city = None
        if province:
            self.province = province.lower()
        else:
            self.province = None

    @property
    def month_names(self):
        return (
            "Gennaio",
            "Febbraio",
            "Marzo",
            "Aprile",
            "Maggio",
            "Giugno",
            "Luglio",
            "Agosto",
            "Settembre",
            "Ottobre",
            "Novembre",
            "Dicembre",
        )

    @property
    def first_day_of_week(self):
        return calendar.MONDAY

    def get_holidays(self, year):
        """Italian holidays for a selected year.

        Info taken from:
        - http://www.timeanddate.com/holidays/italy/
        - http://www.qppstudio.net/publicholidays2015/italy.htm
        - https://it.wikipedia.org/wiki/Pentecoste
        """
        hols = super().get_holidays(year)
        hols.append(date(year, 1, 1))  # New Year
        hols.append(date(year, 1, 6))  # Epiphany
        hols.append(date(year, 4, 25))  # Liberation Day (St. Mark)
        hols.append(date(year, 5, 1))  # Labour Day
        hols.append(date(year, 6, 2))  # Republic Day
        if self.city in ["firenze", "genova", "torino"]:
            hols.append(date(year, 6, 24))  # St. Giovanni
        if self.city == "roma":
            hols.append(date(year, 6, 29))  # St. Peter & Paul
        if self.city == "palermo":
            hols.append(date(year, 7, 15))  # St. Rosalia
        hols.append(date(year, 8, 15))  # Assumption of Mary
        if self.city == "napoli":
            hols.append(date(year, 9, 19))  # St. Gennaro
        if self.city == "bologna":
            hols.append(date(year, 10, 4))  # St. Petronio
        if self.city == "cagliari":
            hols.append(date(year, 10, 30))  # St. Saturnio
        hols.append(date(year, 11, 1))  # All Saints' Day
        if self.city == "trieste":
            hols.append(date(year, 11, 3))  # St. Giusto
        if self.city == "bari":
            hols.append(date(year, 12, 6))  # St. Nicola
        if self.city == "milano":
            hols.append(date(year, 12, 7))  # St. Ambrose
        hols.append(date(year, 12, 8))  # Immaculate Conception
        hols.append(date(year, 12, 25))  # Christmas Day
        hols.append(date(year, 12, 26))  # St. Stefano

        # Easter (Sunday + Monday)
        hols.append(easter(year))
        hols.append(easter(year) + timedelta(days=1))
        if self.province == "bolzano":
            # Pentecoste (in Alto Adige / Südtirol)
            hols.append(easter(year) + timedelta(days=50))
        return hols

    @property
    def calendar_name(self):
        return "Calendario"
