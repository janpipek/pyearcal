class DefaultLocale(object):
    @property
    def month_names(self):
        return (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        )

    def month_title(self, year, month):
        return "%s %d" % (self.month_names[month - 1], year)

    @property
    def first_day_of_week(self):
        return 0