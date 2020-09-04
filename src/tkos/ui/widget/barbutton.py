from display import TFT
from tkos.ui.widget.rectangle import Rectangle
from tkos.ui.widget.padding import Padding
from tkos.ui.widget.label import Label
from tkos.ui.widget import Alignment

class BarButton(Rectangle):
    def __init__(self, x, y, width=None, height=None, display=None, parent=None, fgcolor=TFT.WHITE, bgcolor=TFT.ORANGE, padding=Padding.small(), text=None):
        
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._padding = padding
        self._text = text

        # TODO: Expose properties of all widgets

        self._label = Label(0, 0, color=fgcolor, text=self._text)
        calc_width = width or self._label._width + padding.pad_left + padding.pad_right
        calc_height = height or self._label._height + padding.pad_top + padding.pad_bottom

        super().__init__(x, y, calc_width, calc_height, display, parent, bgcolor)
        self.addChild(self._label)
        self._label.align(alignment=Alignment())