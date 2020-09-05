from display import TFT
from tkos.ui.widget.rectangle import Rectangle
from tkos.ui.widget.padding import Padding
from tkos.ui.widget.label import Label
from tkos.ui.widget import Alignment, Widget

class BarButton(Rectangle):
    """A button to be used in a bar or in a list."""
    def __init__(self, x:int, y:int, width:int=None, height:int=None, display:TFT=None, parent:Widget=None, fgcolor=TFT.WHITE, bgcolor=TFT.ORANGE, padding:Padding=Padding.small(), text:str=''):
        """Creates a new bar button

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            width (int, optional): The width, inferred from text and padding if None. Defaults to None.
            height (int, optional): The height, inferred from text and padding if None. Defaults to None.
            display (TFT, optional): The display to use. Defaults to the primary display.
            parent (Widget, optional): The parent widget. Defaults to None.
            fgcolor (int, optional): The foreground color. Defaults to TFT.WHITE.
            bgcolor (int, optional): The background color. Defaults to TFT.ORANGE.
            padding (Padding, optional): The inner padding. Defaults to Padding.small().
            text (str, optional): The inner label's text. Defaults to an empty string.
        """
        # --- Set variables ---
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._padding = padding
        self._text = text

        # --- Set children and calculate its size ---
        self._label = Label(0, 0, color=fgcolor, text=self._text)
        calc_width = width or self._label._width + padding.pad_left + padding.pad_right
        calc_height = height or self._label._height + padding.pad_top + padding.pad_bottom

        # --- Add the child to the children list and align it after super init ---
        super().__init__(x, y, calc_width, calc_height, display, parent, bgcolor)
        self.addChild(self._label)
        self._label.align(alignment=Alignment())

    # ---------- Properties ----------

    # ----- Foreground color property -----

    def __get_fgcolor(self):
        return self._fgcolor

    def __set_fgcolor(self, fgcolor):
        self._fgcolor = fgcolor
        self.draw()

    fgcolor = property(__get_fgcolor, __set_fgcolor)


    # ----- Background color property -----

    def __get_bgcolor(self):
        return self._bgcolor

    def __set_bgcolor(self, bgcolor):
        self._bgcolor = bgcolor
        self.draw()

    bgcolor = property(__get_bgcolor, __set_fgcolor)


    # ----- Padding property -----

    def __get_padding(self):
        return self._padding

    def __set_padding(self, padding:Padding):
        self._padding = padding
        self.draw()

    padding = property(__get_padding, __set_fgcolor)


    # ----- Text property -----

    def __get_text(self):
        return self._text

    def __set_text(self, text):
        self.clear()
        self._text = text
        self._label.text = text
        self.draw()

    text = property(__get_text, __set_fgcolor)
