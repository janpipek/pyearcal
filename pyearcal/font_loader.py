"""font_loader module

This modules enables (and automatically performs) loading
of TTF fonts.

By default, it loads some Microsoft fonts using load_standard_windows_fonts()
and a few open-source fonts in load_standard_open_source_fonts().

However, you can add your fonts using load_ttf_font().

"""
import logging
import os
import warnings

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab import rl_config

from fontTools import ttLib

# Define font variant names
BOLD = "bold"
LIGHT = "light"
LIGHT_ITALIC = "lightItalic"
ITALIC = "italic"
ITALIC_BOLD = "italicBold"
NORMAL = "normal"

# Aliases
BOOK = NORMAL
REGULAR = NORMAL
OBLIQUE = ITALIC
BOLD_ITALIC = ITALIC_BOLD

defaultSuffixes = {
    NORMAL: "",
    BOLD: "b",
    ITALIC: "i",
    ITALIC_BOLD: "z",
    LIGHT: "l",
    LIGHT_ITALIC: "li",
}


class FontNotFound(RuntimeError):
    pass


def load_ttf_font(font_name, variants, verbose=True):
    """Try to load TTF font.

    :param variants: dictionary of variants and corresponding file names.

    It tries to find the font in all directories reportlab looks in (+ few others).
    It uses a few different extensions (ttf, otf, ttc + caps alternatives)
    """
    kwargs = {}
    # if verbose:
    #     print(font_name)
    #     print(variants)
    for key, file_name in variants.items():
        if file_name:
            for extension in ".ttf", ".otf", ".ttc", ".TTF", ".OTF", ".TTC":
                try:
                    registered_name = _get_font_name(font_name, key)

                    pdfmetrics.registerFont(TTFont(registered_name, file_name + extension))
                    kwargs[key] = registered_name
                    # print("{0}:{1}".format(font_name, file_name + extension))
                    break
                except TTFError as e:
                    # print(e)
                    # if 'postscript outlines are not supported' in e.:
                    #     print(e)
                    pass
                except Exception as e:
                    # print e
                    pass
    try:
        if len(kwargs):
            if verbose:
                logging.info("Font '%s' found (%s)" % (font_name, ", ".join(kwargs.keys())))
            pdfmetrics.registerFontFamily(font_name, **kwargs)
            return True
    except:
        return False


def _suffixify(base_name, **kwargs):
    """Guess variant font file names.

    Uses defaultSuffixes and overrides them with supplied kwargs.
    Returns a dictionary with file names without file extensions.
    """
    all_variants = {}
    all_variants.update(defaultSuffixes)
    all_variants.update(**kwargs)
    return {variant: base_name + suffix for variant, suffix in all_variants.items()}


def _get_font_name(font_name, variant):
    return font_name + "-" + variant


def get_font_name(font_name, variant=NORMAL, require_exact=False):
    """Get name under which the font is registered in PDF metrics.

    :param font_name: The basic name of the font (like 'Arial', ...)
    :param variant: Variant of the file name (like 'normal', 'italic', ...)
    :param require_exact: Use normal variant as fall-back.

    Tries to find the font. If not found, it can either fallback to
    normal variant or throw exception.
    """
    key = _get_font_name(font_name, variant)

    if not key in pdfmetrics.getRegisteredFontNames():
        try_load_font_mpl(font_name)

    if not key in pdfmetrics.getRegisteredFontNames():
        if require_exact:
            raise Exception("Font '%s', variant '%s' does not exist." % (font_name, variant))
        else:
            key = _get_font_name(font_name, variant=NORMAL)
            if not key in pdfmetrics.getRegisteredFontNames():
                raise Exception("Font '%s' does not exist." % (font_name))
            else:
                print(
                    "Font '%s', variant '%s' does not exist, using 'normal' instead."
                    % (font_name, variant)
                )
    return key


def get_loaded_fonts():
    """List all loaded fonts.

    :rtype: list
    """
    return pdfmetrics.getRegisteredFontNames()


def load_standard_windows_fonts():
    """Load fonts that normally exist in Windows / Office."""
    load_ttf_font("Arial", _suffixify("arial", bold="bd", italicBold="bi"))
    load_ttf_font("Calibri", _suffixify("calibri"))
    load_ttf_font("Cambria", _suffixify("cambria"))
    load_ttf_font("Candara", _suffixify("Candara"))
    load_ttf_font("Comic Sans", _suffixify("comic", bold="bd"))
    load_ttf_font("Constantia", _suffixify("constan"))
    load_ttf_font("Corbel", _suffixify("corbel"))
    load_ttf_font("Courier New", _suffixify("cour", bold="bd", italicBold="bi"))
    load_ttf_font("Garamond", _suffixify("GARA", bold="BD", italic="IT"))
    load_ttf_font("Georgia", _suffixify("georgia"))
    load_ttf_font("Tahoma", _suffixify("tahoma", bold="bd"))
    load_ttf_font("Times New Roman", _suffixify("times", bold="bd", italicBold="bi"))
    load_ttf_font("Trebuchet", _suffixify("trebuc", bold="bd", italic="it", italicBold="bi"))
    load_ttf_font("Verdana", _suffixify("verdana"))


def load_standard_open_source_fonts():
    """Load fonts that usually come with open-source software."""
    load_ttf_font(
        "DejaVu Sans",
        _suffixify("DejaVuSans", bold="-Bold", italic="-Oblique", italicBold="-BoldOblique"),
    )
    load_ttf_font(
        "DejaVu Sans Condensed",
        _suffixify(
            "DejaVuSansCondensed", bold="-Bold", italic="-Oblique", italicBold="-BoldOblique"
        ),
    )
    load_ttf_font(
        "DejaVu Serif",
        _suffixify("DejaVuSerif", bold="-Bold", italic="-Oblique", italicBold="-BoldOblique"),
    )
    load_ttf_font(
        "DejaVu Serif Condensed",
        _suffixify(
            "DejaVuSerifCondensed", bold="-Bold", italic="-Oblique", italicBold="-BoldOblique"
        ),
    )
    load_ttf_font("Gentium", _suffixify("Gen", normal="R102", italic="I102"))
    load_ttf_font(
        "Gentium Basic", _suffixify("GenBas", normal="R", bold="B", italic="I", italicBold="BI")
    )
    load_ttf_font(
        "Gentium Book Basic",
        _suffixify("GenBkBas", normal="R", bold="B", italic="I", italicBold="BI"),
    )
    load_ttf_font(
        "Liberation Sans",
        _suffixify(
            "LiberationSans",
            normal="-Regular",
            bold="-Bold",
            italic="-Italic",
            italicBold="-BoldItalic",
        ),
    )
    load_ttf_font(
        "Liberation Serif",
        _suffixify(
            "LiberationSerif",
            normal="-Regular",
            bold="-Bold",
            italic="-Italic",
            italicBold="-BoldItalic",
        ),
    )
    load_ttf_font(
        "STIX",
        _suffixify(
            "STIX", normal="-Regular", bold="-Bold", italic="-Italic", italicBold="-BoldItalic"
        ),
    )
    load_ttf_font("Cantarell", _suffixify("Cantarell", normal="-Regular", bold="-Bold"))


def load_system_fonts():
    from matplotlib.font_manager import findSystemFonts

    fonts = findSystemFonts()
    families = {get_font_family(font) for font in fonts}
    for family in families:
        try_load_font_mpl(family)


def try_load_font_mpl(name):
    try:
        from matplotlib.font_manager import FontManager
    except ImportError:
        return

    fm = FontManager()
    suggestions = {}

    for style in [BOLD, LIGHT, LIGHT_ITALIC, ITALIC, ITALIC_BOLD, NORMAL]:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            suggestion = fm.findfont(
                "{0}:{1}".format(name, style.lower()), fallback_to_default=True
            )
        if get_font_family(suggestion) != name:
            continue
        else:
            add_font_directory(os.path.dirname(suggestion))
            suggestions[style] = suggestion

    load_ttf_font(
        name,
        {
            style: os.path.splitext(os.path.basename(suggestion))[0]
            for style, suggestion in suggestions.items()
        },
    )


def get_font_family(path):
    """Get the short name from the font's names table"""
    name = ""
    family = ""

    font = ttLib.TTFont(path)

    FONT_SPECIFIER_NAME_ID = 4
    FONT_SPECIFIER_FAMILY_ID = 1

    for record in font["name"].names:
        if b"\x00" in record.string:
            name_str = record.string.decode("utf-16-be", errors="replace")
        else:
            name_str = record.string.decode("utf-8", errors="replace")
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family:
            break
    return family


def add_font_directory(directory, walk=True):
    directory = os.path.expanduser(directory)
    all_dirs = [directory]
    if walk:
        for current, dirs, _ in os.walk(directory):
            all_dirs += [os.path.join(current, d) for d in dirs]
    rl_config.TTFSearchPath = tuple(list(rl_config.TTFSearchPath) + all_dirs)
    # print(rl_config.TTFSearchPath)


# Hack to browse through all directories in /usr/share/fonts
if os.name == "posix":
    add_font_directory("/usr/share/fonts", True)

add_font_directory(".")

# load_system_fonts()
# load_standard_windows_fonts()
# load_standard_open_source_fonts()
