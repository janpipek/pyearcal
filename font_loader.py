from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BOLD = "bold"
LIGHT = "light"
LIGHT_ITALIC = "lightItalic"
ITALIC = "italic"
ITALIC_BOLD = "italicBold"
NORMAL = "normal"

BOOK = NORMAL
OBLIQUE = ITALIC

defaultSuffixes = {
    NORMAL : "",
    BOLD : "b",
    ITALIC : "i",
    ITALIC_BOLD : "z",
    LIGHT : "l",
    LIGHT_ITALIC : "li"
}

def load_ttf_font(font_name, variants):
    for key, file_name in variants.items():
        if file_name:
            for extension in ".ttf", ".otf", ".ttc", ".TTF":
                try:
                    registered_name = _get_font_name(font_name, key)
                    pdfmetrics.registerFont(TTFont(registered_name, file_name + extension))
                    kwargs[key] = registered_name
                    break
                except:
                    pass
    try:
        pdfmetrics.registerFontFamily(font_name, **kwargs)
    except:
        pass
    

def _suffixify(base_name, **kwargs):
    all_variants = {}
    all_variants.update(defaultSuffixes)
    all_variants.update(**kwargs)
    return { variant : base_name + suffix for variant, suffix in all_variants.items() }

def _get_font_name(font_name, variant):
    return font_name + "-" + variant

def get_font_name(font_name, variant=NORMAL, require_exact=False):
    key = _get_font_name(font_name, variant)
    if not key in pdfmetrics.getRegisteredFontNames():
        if require_exact:
            raise Exception("Font '%s', variant '%s' does not exist." % (font_name, variant))
        else:
            key = _get_font_name(font_name, variant=NORMAL)
            if not key in pdfmetrics.getRegisteredFontNames():
                raise Exception("Font '%s' does not exist." % (font_name))
            else:
                print "Font '%s', variant '%s' does not exist, using 'normal' instead." % (font_name, variant)
    return key

def load_standard_windows_fonts():
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
    load_ttf_font("DejaVu Sans", _suffixify("DejaVuSans", bold="-Bold",
        italic="-Oblique", italicBold="-BoldOblique"))
    load_ttf_font("DejaVu Sans Condensed", _suffixify("DejaVuSansCondensed", bold="-Bold",
        italic="-Oblique", italicBold="-BoldOblique"))
    load_ttf_font("DejaVu Serif", _suffixify("DejaVuSerif", bold="-Bold",
        italic="-Oblique", italicBold="-BoldOblique"))
    load_ttf_font("DejaVu Serif Condensed", _suffixify("DejaVuSerifCondensed", bold="-Bold",
        italic="-Oblique", italicBold="-BoldOblique"))
    load_ttf_font("Gentium Basic", _suffixify("GenBas", normal="R", bold="B",
        italic="I", italicBold="BI"))
    load_ttf_font("Gentium Book Basic", _suffixify("GenBkBas", normal="R", bold="B",
        italic="I", italicBold="BI"))

load_standard_windows_fonts()
load_standard_open_source_fonts()

print "Registered %d font variants:" % len(pdfmetrics.getRegisteredFontNames())
print "-----------------"
for font in pdfmetrics.getRegisteredFontNames():
    print font
print "-----------------"