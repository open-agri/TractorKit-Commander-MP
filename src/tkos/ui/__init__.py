from display import TFT
from tkos.ui.widget import Widget, WidgetDrawer, Alignment
from tkos.ui.widget.rectangle import Rectangle
from tkos.ui.widget.label import Label
from tkos.ui.widget.barbutton import BarButton



class UI:
    """The TKOS user interface."""
    def __init__(self, tft: TFT):
        """Initializes the user interface.

        Args:
            tft (TFT): The display to use for the UI.
        """
        WidgetDrawer.init(tft)

        # test
        self.x = Widget(10, 10, 40, 40)  # , color=TFT.GREEN)
        self.y = Rectangle(30, 20, 30, 20, parent=self.x, color=TFT.BLUE)
        self.x.move(x=100, y=100)
        self.x.resize(width=200, height=150)
        self.y.resize(100, 100)

        self.t = BarButton(20, 30, parent=self.y, text="Button")

        self.y.align(alignment=Alignment())
        self.t.align(alignment=Alignment())
