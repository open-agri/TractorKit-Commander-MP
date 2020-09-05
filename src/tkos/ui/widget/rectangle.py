from display import TFT
from tkos.ui.widget import Widget

class Rectangle(Widget):
    """A filled rectangular widget."""
    def __init__(self, x, y, width, height, display = None, parent = None, color = TFT.WHITE):
        self._bgcolor = color
        super().__init__(x, y, width, height, display, parent)

    # ---------- Properties ----------

    # ----- Background color property -----

    def __get_bgcolor(self):
        return self._bgcolor

    def __set_bgcolor(self, color):
        self._bgcolor = color
        self.drawTree()

    bgcolor = property(__get_bgcolor, __set_bgcolor)

    # ---------- Functions ----------

    def draw(self):
        """Draws this rectangle."""
        print("Drawing", self, "at", (self.x, self.y, self.width, self.height), "in window of size", self._display.winsize())
        self._display.rect(self.x, self.y, self.width, self.height, color = self._bgcolor, fillcolor = self._bgcolor)
