#!/usr/bin/env python
from datetime import date
import logging

import click

from pyearcal.year_calendar import YearCalendar
from pyearcal.l10n import get_locale
from pyearcal.image_sources import UnsortedImageDirectory, SortedImageDirectory


def load_special_days(path, year):
    """Load special days from external file.

    The file is expected to have lines of MM, DD format
    """
    with open(path, "r") as f:
        days = []
        for line in f:
            month, day = [int(s.strip()) for s in line.split(",")]
            days.append(date(year, month, day))
        return days


@click.command()
@click.argument("output", default="calendar.pdf")
@click.option("-s", "--source", type=click.Path(), default=".")
@click.option(
    "-l", "--locale", type=click.Choice(["en", "cs", "it", "sk"]), default="en"
)
@click.option("-y", "--year", default=date.today().year + 1, type=int)
@click.option("-f", "--font", type=str)
@click.option("-d", "--special-days", type=str)
@click.option("--sorted/--unsorted", default=False)
@click.option("-v", "--verbose", count=True)
def run(
    output, source, locale, year, special_days=None, font=None, sorted=False, verbose=0
):
    """Generate year calendar."""
    if verbose:
        if verbose == 1:
            logging.basicConfig(level=logging.INFO)
        if verbose == 2:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.warn("Invalid verbosity level (available: 0..2)")

    if sorted:
        image_source = SortedImageDirectory(source)
    else:
        image_source = UnsortedImageDirectory(source)
    locales = get_locale(locale)
    kwargs = {}
    if font:
        kwargs["title_font_name"] = font
        kwargs["cell_font_name"] = font
    if special_days:
        kwargs["special_days"] = load_special_days(special_days, year)
    calendar = YearCalendar(year, image_source, locales, **kwargs)
    calendar.render(output)


if __name__ == "__main__":
    run()
