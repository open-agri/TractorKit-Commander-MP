from tkos.ui.widget import Widget
from display import TFT

class Rectangle(Widget):
    def __init__(self, x, y, width, height, display = None, parent = None, color = TFT.WHITE):
        self._bgcolor = color
        super().__init__(x, y, width, height, display, parent)

    def __draw(self):
        self._display.rect(self._x, self._y, self._width, self._height, color = self._bgcolor, fillcolor = self._bgcolor)