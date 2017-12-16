from .default import DefaultLocale

from .czech import CzechLocale
from .slovak import SlovakLocale
from .italian import ItalianLocale


def get_locale(locale):
    if locale == "us":
        return DefaultLocale()
    elif locale == "cs":
        return CzechLocale()
    elif locale == "sk":
        return SlovakLocale()
    elif locale == "it":
        return ItalianLocale()
    else:
        raise ValueError("Unknown locale")
