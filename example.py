# Import important modules
from pyearcal import YearCalendar
# from image_sources import UnsortedImageDirectory
from datetime import date
from l18n import DefaultLocale
from flickr_downloader import FlickrDownloader

# Use all pictures from "images" directory
image_source = FlickrDownloader("skyscraper")

# Use Czech locale and holidays
locale = DefaultLocale()

# Set a few special days
special_days = [
    date(2014, 1, 31) # Guido van Rossum's birthday
]

calendar = YearCalendar(2014, image_source, locale, special_days)
calendar.render("calendar.pdf")