"""font_loader module

This module enables loading of TTF/OTF fonts into reportlab.

You can add your fonts using load_ttf_font() or try_load_font_mpl().

"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import rl_config

# Define font variant names
BOLD = "bold"
ITALIC = "italic"
BOLD_ITALIC = "boldItalic"
NORMAL = "normal"

# Aliases for convenience
REGULAR = NORMAL
OBLIQUE = ITALIC
ITALIC_BOLD = BOLD_ITALIC

# Extensions to try when searching for font files
FONT_EXTENSIONS = (".ttf", ".otf", ".ttc", ".TTF", ".OTF", ".TTC")


class FontNotFound(RuntimeError):
    pass


def _get_font_name(font_name: str, variant: str) -> str:
    """Generate the registered name for a font variant."""
    return f"{font_name}-{variant}"


def _find_font_file(base_name: str) -> Optional[str]:
    """Find a font file in reportlab's search paths.
    
    Returns the full path to the font file if found, None otherwise.
    """
    # Try with various extensions
    for ext in FONT_EXTENSIONS:
        filename = base_name + ext
        
        # Check if it's an absolute path that exists
        if os.path.isabs(filename) and os.path.isfile(filename):
            return filename
        
        # Check current directory
        if os.path.isfile(filename):
            return os.path.abspath(filename)
        
        # Check reportlab's search paths
        for search_dir in rl_config.TTFSearchPath:
            full_path = os.path.join(search_dir, filename)
            if os.path.isfile(full_path):
                return full_path
    
    return None


def load_ttf_font(font_name: str, variants: Dict[str, str]) -> bool:
    """Load TTF font with specified variants.

    :param font_name: The name to register the font family under.
    :param variants: Dictionary mapping variant names (normal, bold, italic, boldItalic)
                     to file names (without extension).
    :returns: True if at least one variant was loaded successfully.
    
    Example:
        load_ttf_font("Arial", {
            "normal": "arial",
            "bold": "arialbd", 
            "italic": "ariali",
            "boldItalic": "arialbi"
        })
    """
    registered_variants = {}
    
    for variant, base_filename in variants.items():
        if not base_filename:
            continue
            
        font_path = _find_font_file(base_filename)
        if font_path is None:
            logging.debug(f"Font file not found for {font_name} variant {variant}: {base_filename}")
            continue
        
        registered_name = _get_font_name(font_name, variant)
        
        try:
            pdfmetrics.registerFont(TTFont(registered_name, font_path))
            registered_variants[variant] = registered_name
            logging.debug(f"Loaded font {registered_name} from {font_path}")
        except Exception as exc:
            logging.warning(f"Failed to load font {registered_name} from {font_path}: {exc}")
    
    if not registered_variants:
        logging.debug(f"No variants found for font '{font_name}'")
        return False
    
    # Register font family with reportlab
    # Only use the standard variant names that registerFontFamily accepts
    family_kwargs = {}
    if NORMAL in registered_variants:
        family_kwargs["normal"] = registered_variants[NORMAL]
    if BOLD in registered_variants:
        family_kwargs["bold"] = registered_variants[BOLD]
    if ITALIC in registered_variants:
        family_kwargs["italic"] = registered_variants[ITALIC]
    if BOLD_ITALIC in registered_variants:
        family_kwargs["boldItalic"] = registered_variants[BOLD_ITALIC]
    
    if family_kwargs:
        try:
            pdfmetrics.registerFontFamily(font_name, **family_kwargs)
            logging.info(f"Font '{font_name}' loaded with variants: {', '.join(registered_variants.keys())}")
        except Exception as exc:
            logging.warning(f"Failed to register font family '{font_name}': {exc}")
    
    return True


def get_font_name(
    font_name: str, variant: str = NORMAL, require_exact: bool = False
) -> str:
    """Get name under which the font is registered in PDF metrics.

    :param font_name: The basic name of the font (like 'Arial', ...)
    :param variant: Variant of the font (normal, bold, italic, boldItalic)
    :param require_exact: If True, raise error when exact variant not found.
                          If False, fall back to normal variant.
    :returns: The registered font name to use with reportlab.
    :raises FontNotFound: If the font (or required variant) is not available.
    """
    key = _get_font_name(font_name, variant)

    if key not in pdfmetrics.getRegisteredFontNames():
        # Try to load the font using matplotlib
        try_load_font_mpl(font_name)

    if key not in pdfmetrics.getRegisteredFontNames():
        if require_exact:
            raise FontNotFound(
                f"Font '{font_name}', variant '{variant}' does not exist."
            )
        else:
            # Fall back to normal variant
            key = _get_font_name(font_name, variant=NORMAL)
            if key not in pdfmetrics.getRegisteredFontNames():
                raise FontNotFound(f"Font '{font_name}' does not exist.")
            else:
                logging.info(
                    f"Font '{font_name}', variant '{variant}' "
                    "not found, using 'normal' instead."
                )
    return key


def get_loaded_fonts() -> List[str]:
    """List all loaded font names."""
    return list(pdfmetrics.getRegisteredFontNames())


def try_load_font_mpl(name: str) -> bool:
    """Try to load a font by name using matplotlib's font manager.
    
    :param name: Font family name (e.g., "Arial", "DejaVu Sans")
    :returns: True if the font was loaded successfully.
    """
    try:
        from matplotlib.font_manager import fontManager
    except ImportError:
        logging.debug("matplotlib not available for font discovery")
        return False

    variants_to_find = {
        NORMAL: {"weight": "normal", "style": "normal"},
        BOLD: {"weight": "bold", "style": "normal"},
        ITALIC: {"weight": "normal", "style": "italic"},
        BOLD_ITALIC: {"weight": "bold", "style": "italic"},
    }
    
    found_variants = {}
    
    for font_entry in fontManager.ttflist:
        if font_entry.name != name:
            continue
        
        font_path = font_entry.fname
        if not os.path.isfile(font_path):
            continue
        
        # Determine which variant this font file represents
        weight = font_entry.weight
        style = font_entry.style
        
        # Map matplotlib weight/style to our variant names
        is_bold = weight in ("bold", "demibold", "heavy", "black", 600, 700, 800, 900)
        is_italic = style in ("italic", "oblique")
        
        if is_bold and is_italic:
            variant = BOLD_ITALIC
        elif is_bold:
            variant = BOLD
        elif is_italic:
            variant = ITALIC
        else:
            variant = NORMAL
        
        # Only use first match for each variant
        if variant not in found_variants:
            found_variants[variant] = font_path
    
    if not found_variants:
        logging.debug(f"Font '{name}' not found via matplotlib")
        return False
    
    # Register the found fonts
    registered_variants = {}
    for variant, font_path in found_variants.items():
        registered_name = _get_font_name(name, variant)
        try:
            pdfmetrics.registerFont(TTFont(registered_name, font_path))
            registered_variants[variant] = registered_name
            logging.debug(f"Loaded font {registered_name} from {font_path}")
        except Exception as exc:
            logging.warning(f"Failed to load font {registered_name} from {font_path}: {exc}")
    
    if not registered_variants:
        return False
    
    # Register font family
    family_kwargs = {}
    if NORMAL in registered_variants:
        family_kwargs["normal"] = registered_variants[NORMAL]
    if BOLD in registered_variants:
        family_kwargs["bold"] = registered_variants[BOLD]
    if ITALIC in registered_variants:
        family_kwargs["italic"] = registered_variants[ITALIC]
    if BOLD_ITALIC in registered_variants:
        family_kwargs["boldItalic"] = registered_variants[BOLD_ITALIC]
    
    if family_kwargs:
        try:
            pdfmetrics.registerFontFamily(name, **family_kwargs)
            logging.info(f"Font '{name}' loaded via matplotlib with variants: {', '.join(registered_variants.keys())}")
        except Exception as exc:
            logging.warning(f"Failed to register font family '{name}': {exc}")
    
    return True


def add_font_directory(directory: str, walk: bool = True) -> None:
    """Add a directory to reportlab's font search path.
    
    :param directory: Directory path to add.
    :param walk: If True, also add all subdirectories.
    """
    directory = os.path.expanduser(directory)
    if not os.path.isdir(directory):
        return
    
    all_dirs = [directory]
    if walk:
        for current, dirs, _ in os.walk(directory):
            all_dirs.extend(os.path.join(current, d) for d in dirs)
    
    # Add to reportlab's search path
    current_paths = list(rl_config.TTFSearchPath)
    for d in all_dirs:
        if d not in current_paths:
            current_paths.append(d)
    rl_config.TTFSearchPath = tuple(current_paths)


def load_font_from_path(font_name: str, font_path: str, variant: str = NORMAL) -> bool:
    """Load a single font file with an explicit path.
    
    :param font_name: The name to register the font under.
    :param font_path: Full path to the font file.
    :param variant: Which variant this font represents (normal, bold, italic, boldItalic).
    :returns: True if the font was loaded successfully.
    """
    if not os.path.isfile(font_path):
        logging.warning(f"Font file not found: {font_path}")
        return False
    
    registered_name = _get_font_name(font_name, variant)
    
    try:
        pdfmetrics.registerFont(TTFont(registered_name, font_path))
        logging.info(f"Loaded font {registered_name} from {font_path}")
        return True
    except Exception as exc:
        logging.warning(f"Failed to load font {registered_name} from {font_path}: {exc}")
        return False


# Initialize search paths
if os.name == "posix":
    add_font_directory("/usr/share/fonts", walk=True)
    add_font_directory("~/.fonts", walk=True)
    add_font_directory("~/.local/share/fonts", walk=True)

if os.name == "nt":
    # Windows fonts directory
    windir = os.environ.get("WINDIR", "C:\\Windows")
    add_font_directory(os.path.join(windir, "Fonts"), walk=False)

add_font_directory(".", walk=False)
