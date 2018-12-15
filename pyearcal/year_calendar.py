from __future__ import division, absolute_import

import logging

from calendar import Calendar

import PIL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from .l10n import DefaultLocale
from . import font_loader


class YearCalendar(object):
    '''A year calendar with 12 pages for each month.

    All attributes have reasonable defaults.
    However, they can be overridden in constructor as well as directly.

    The most important method is "render" that renders the calendar
    into a specified file.

    Fonts:
        Any font can be used. Reportlab by default uses Adobe fonts.
        Module font_loader however tries to import as many system fonts (TTF)
        as possible (see there). You can register your own fonts as well.

    Scaling algorithms:
        These algorithms (as scaling attribute) determine how the
        pictures are scaled (and transformed) to fit in the desired area.

        - "squarecrop" : Take square area and put a cropped picture inside
        - "fit" : Take the largest area possible and fit the whole image inside

    Attributes:
    - holidays: A list of datetime.date's (default: from locale)
    - pagesize: (width, height) in points (default: A4)
    - scaling: Scaling algorithm (default: squarecrop, see above)
    - margins: (top, right, bottom, left) in points (default: 1.33cm)

    - title_font_name: Name of a registered font (see above)
    - title_font_size: Month title font size in pt (default 24)
    - title_font_variant: Month title font variant (see font_loader)

    - include_year_in_month_name

    '''

    def __init__(self, year, pictures, locale=DefaultLocale(), special_days=[], **kwargs):
        """Constructor with all initialization.

        :param year: The year in YYYY format.
        :param pictures: A picture source (collection with indexes 1..12).
        :param scaling: Algorithm for scaling pictures (default squarecrop, see)
        :param kwargs: A dictionary of attributes to be overridden (see class description)
        """
        self.year = year
        self.pictures = pictures
        self.locale = locale
        self.special_days = special_days

        self.scaling = kwargs.get("scaling", "squarecrop")
        self.holidays = kwargs.get("holidays", self.locale.holidays(self.year))
        self.pagesize = kwargs.get("pagesize", A4)
        self.margins = kwargs.get("margins", (1.33*cm,) * 4)   # top, right, bottom, left

        self.max_table_height = kwargs.get("max_table_height", self.content_height / 4)

        self.title_font_name = kwargs.get("title_font_name", "DejaVu Sans")
        self.title_font_variant = kwargs.get("title_font_variant", font_loader.BOLD)
        self.title_margin = kwargs.get("title_margin", 6 * mm)
        self.title_font_size = kwargs.get("title_font_size", 24) #pt

        self.cell_font_name = kwargs.get("cell_font_name", "DejaVu Sans")
        self.cell_font_variant = kwargs.get("cell_font_variant", font_loader.NORMAL)
        self.cell_font_size = kwargs.get("cell_font_size", 16) #pt
        self.cell_padding = kwargs.get("cell_padding", 6)
        self.cell_spacing = kwargs.get("cell_spacing", 2 * mm)

        self.week_color = kwargs.get("week_color", colors.Color(0.2, 0.2, 0.2))
        self.week_bgcolor = kwargs.get("week_bgcolor", colors.white)
        self.weekend_color = kwargs.get("weekend_color", colors.white)
        self.weekend_bgcolor = kwargs.get("weekend_bgcolor", colors.Color(0.7, 0.7, 0.7))
        self.holiday_color = kwargs.get("holiday_color", self.weekend_color)
        self.holiday_bgcolor = kwargs.get("holiday_bgcolor", colors.Color(0.4, 0.4, 0.4))
        self.special_day_color = kwargs.get("special_day_color", colors.white)
        self.special_day_bgcolor = kwargs.get("special_day_bgcolor", colors.Color(0.2, 0.2, 0.2))

        self.include_year_in_month_name = kwargs.get("include_year_in_month_name", False)

        # Initialize calendar
        self._calendar = Calendar(self.locale.first_day_of_week)

    def _repr_html_(self):
        """HTML representation, useful for IPython notebook."""
        from io import BytesIO
        from base64 import b64encode
        html = "<div>"
        html += "<div style='font-size:124%'>Calendar for year {0}</div>".format(self.year)
        html += "<div>"
        thumb_size = 64
        for i, image in enumerate(self.pictures):
            pil_im = PIL.Image.open(image)
            pil_im = self._scale_picture(pil_im, 1)[0]
            pil_im.thumbnail((thumb_size, thumb_size))
            b = BytesIO()
            pil_im.save(b, format='png')
            image_data = b64encode(b.getvalue()).decode('utf-8')
            html += "<img style='display:inline-block; margin:1px' alt='{0}' src='data:image/png;base64,{1}'/>".format(i, image_data)
        html += "</div>"
        html += "</div>"
        return html

    @property
    def width(self):
        return self.pagesize[0]

    @property
    def height(self):
        return self.pagesize[1]

    @property
    def content_width(self):
        '''Content width (= paper width - margins).'''
        return self.width - self.margins[1] - self.margins[3]

    @property
    def content_height(self):
        '''Content height (= paper height - margins).'''
        return self.height - self.margins[0] - self.margins[2]

    @property
    def cell_height(self):
        '''Height of a day cell in month calendar.'''
        return self.max_table_height / 6

    @property
    def cell_width(self):
        '''Width of a day cell in month calendar.'''
        return self.content_width / 7

    def set_font(self, name, size=12, variant="normal"):
        font = font_loader.get_font_name(name, variant)
        self.canvas.setFont(font, size)

    def _style_holidays_and_special_days(self, month, table_style):
        '''Set colours for all cells based on categories.

        Categories: weekend, holidays, special days.
        '''
        calendar = self._calendar.monthdatescalendar(self.year, month)
        for row, days in enumerate(calendar):
            for column, day in enumerate(days):
                if day.month != month:
                    continue
                if day.weekday() in self.locale.weekend:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.weekend_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.weekend_color)
                if day in self.holidays:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.holiday_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.holiday_color)
                if day in self.special_days:
                    table_style.add("BACKGROUND", (column, row), (column, row), self.special_day_bgcolor)
                    table_style.add("TEXTCOLOR", (column, row), (column, row), self.special_day_color)

    def _scale_picture(self, image, max_picture_height):
        '''Apply the scaling algorithm.

        :param image: PIL object
        :max_picture_height: the vertical area that can be occupied

        Return tuple (transformed PIL image object, PDF width, PDF height)
        '''
        width, height = image.size

        if self.scaling == "squarecrop":
            crop_size = min(width, height)
            crop_coords = (
                (width - crop_size) // 2,
                (height - crop_size) // 2,
                (width - crop_size) // 2 + crop_size,
                (height - crop_size) // 2 + crop_size
            )
            cropped = image.crop(crop_coords)

            size = min(self.content_width, max_picture_height)
            return cropped, size, size

        elif self.scaling == "fit":
            max_width = self.content_width
            max_height = max_picture_height
            if width * max_height > height * max_width:
                height = max_width * height / width
                width = max_width
            else:
                width = max_height * width / height
                height = max_height
            return image, width, height

        else:
            raise Exception("Unknown scaling: %s" % self.scaling)

    def _render_picture(self, month, max_picture_height):
        '''Draw the picture.

        It is automatically scaled using the selected algorithm.
        '''
        image = PIL.Image.open(self.pictures[month])
        image, width, height = self._scale_picture(image, max_picture_height)
        left = (self.content_width - width) / 2 + self.margins[3]
        top = self.content_height + self.margins[0] - height

        self.canvas.drawImage(ImageReader(image), left, top, width=width, height=height)

    def _render_month(self, month):
        '''Render one page with a month.'''
        
        table_data = self._calendar.monthdayscalendar(self.year, month)
        table_data = [ [ day or None for day in week ] for week in table_data ]

        table = Table(table_data,
            colWidths=(self.cell_width,) * 7,
            rowHeights=(self.cell_height,) * len(table_data)
        )

        style = TableStyle()
        for padding in ("TOP", "RIGHT", "BOTTOM", "LEFT"):
            style.add(padding + "PADDING", (0, 0), (-1, -1), self.cell_padding)
        for position in ("BEFORE", "AFTER", "ABOVE", "BELOW"):
            style.add("LINE" + position, (0, 0), (-1, -1), self.cell_spacing / 2, colors.white)

        font_name = font_loader.get_font_name(self.cell_font_name, self.cell_font_variant)
        style.add("FONT", (0, 0), (-1, -1), font_name, self.cell_font_size)
        style.add("ALIGN", (0, 0), (-1, -1), "LEFT")
        style.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        style.add("BACKGROUND", (0, 0), (-1, -1), self.week_bgcolor)
        style.add("TEXTCOLOR", (0, 0), (-1, -1), self.week_color)

        self._style_holidays_and_special_days(month, style)

        table.setStyle(style)
        table_width, table_height = table.wrapOn(self.canvas, 7*self.cell_width, 6*self.cell_height)
        table.drawOn(self.canvas, self.margins[3], self.margins[2])
        
        # Render title
        title_position = (self.margins[3], self.margins[2] + table_height + self.title_margin)
        self.set_font(self.title_font_name, self.title_font_size, variant=self.title_font_variant)
        self.canvas.drawString(title_position[0], title_position[1], self.locale.month_title(self.year, month, self.include_year_in_month_name))

        # Render picture
        self._render_picture(month, self.content_height - self.title_font_size - 2 * self.title_margin - table_height)
        self.canvas.showPage()

    def render_title_page(self):
        # TODO: Implement
        # self.canvas.showPage()
        pass

    def render(self, file_name):
        '''Render the calendar into a PDF file.

        :param file_name: Path to write to.
        '''
        self.canvas = canvas.Canvas(file_name, self.pagesize)
        self.canvas.setTitle("{0} {1}".format(self.locale.calendar_name, self.year))
        self.render_title_page()   # TODO: To be implemented
        for month in range(1, 13):
            logging.info("Page {0} rendered.".format(month))
            self._render_month(month)
        self.canvas.save()
