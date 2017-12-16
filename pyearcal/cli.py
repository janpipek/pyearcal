#!/usr/bin/env python
from datetime import date

import click
from reportlab.lib import colors

from pyearcal import YearCalendar, font_loader
from pyearcal.l10n import get_locale
from pyearcal.image_sources import UnsortedImageDirectory, SortedImageDirectory


@click.command()
@click.argument("output", default="calendar.pdf")
@click.option("-s", "--source", type=click.Path(), default=".")
@click.option("-l", "--locale", type=click.Choice(['en', 'cs', 'it', 'sk']), default="en")
@click.option("-y", "--year", default=date.today().year+1, type=int)
@click.option("-d", "--special-days", type=str)
def run(output, source, locale, year, special_days=None):
    image_source = UnsortedImageDirectory(source)
    locales = get_locale(locale)
    calendar = YearCalendar(year, image_source, locales, special_days)
    calendar.render(output)


if __name__ == "__main__":
    run()