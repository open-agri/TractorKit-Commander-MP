from display import TFT
from tkos.ui.widget import Widget

class Rectangle(Widget):
    def __init__(self, x, y, width, height, display = None, parent = None, color = TFT.WHITE):
        self._bgcolor = color
        super().__init__(x, y, width, height, display, parent)

        ## TODO: Update on color change

    def draw(self):
        print("Drawing", __name__, "at", (self._x, self._y, self._width, self._height), "in window of size", self._display.winsize())
        self._display.rect(self._x, self._y, self._width, self._height, color = self._bgcolor, fillcolor = self._bgcolor)