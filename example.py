# Import important modules
from pyearcal import YearCalendar
from datetime import date
from l18n import DefaultLocale
from flickr_downloader import FlickrDownloader
from image_sources import SortedImageDirectory
import os

if os.path.exists(".flickr-download"):
    image_source = SortedImageDirectory(".flickr-download")
else:
    # Download a few pictures from a nice region of Ladakh
    image_source = FlickrDownloader("ladakh")

# Use default locale and holidays
locale = DefaultLocale()

# Set a few special days
special_days = [
    date(2014, 1, 31) # Guido van Rossum's birthday
]

calendar = YearCalendar(2014, image_source, locale=locale, scaling="squarecrop", special_days=special_days)
calendar.render("calendar.pdf")