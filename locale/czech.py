# -*- coding: utf-8 -*-

from default import DefaultLocale

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
        return 1        