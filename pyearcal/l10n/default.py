import calendar
from datetime import date
from typing import Collection, Protocol, Tuple


class Locale(Protocol):
    @property
    def month_names(self) -> Collection[str]:
        ...

    @property
    def first_day_of_week(self) -> int:
        ...

    def get_month_title(self, year: int, month: int) -> str:
        ...

    def get_holidays(self, year: int) -> Collection[date]:
        ...

    @property
    def calendar_name(self) -> str:
        ...


class DefaultLocale(Locale):
    """Default calendar.

    In english language, Sunday as first day, no holidays.
    """

    @property
    def month_names(self) -> Tuple[str, ...]:
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
            "December",
        )

    def get_month_title(self, year: int, month: int, include_year: bool = False) -> str:
        if include_year:
            return f"{self.month_names[month - 1]} {year}"
        else:
            return self.month_names[month - 1]

    @property
    def first_day_of_week(self) -> int:
        return calendar.SUNDAY

    @property
    def weekend(self) -> Collection[int]:
        return (calendar.SATURDAY, calendar.SUNDAY)

    def get_holidays(self, year: int) -> Collection[date]:
        return []

    @property
    def calendar_name(self) -> str:
        return "Calendar"
