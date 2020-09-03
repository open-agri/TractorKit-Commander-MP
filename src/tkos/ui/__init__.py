from tkos.ui.widget.rectangle import Rectangle
from tkos.ui.widget import Widget
from display import TFT
from tkos.ui.widget import WidgetDrawer

class UI:
    def __init__(self, tft, width, height):
        WidgetDrawer.init(tft, width, height)


        # test
        self.x = Widget(10, 10, 40, 40)#, color=TFT.GREEN)
        self.y = Rectangle(30, 20, 30, 20, parent=self.x, color=TFT.BLUE)
        self.x.move(x=100, y=100)
        self.x.resize(width=200, height=150)
        self.y.resize(100, 100)
