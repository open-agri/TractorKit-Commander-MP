from tkos.ui.widget import Widget
from tkos.ui.widget import WidgetDrawer

class UI:
    def __init__(self, tft, width, height):
        WidgetDrawer.init(tft, width, height)


        # test
        self.a = Widget(0, 0, 480, 320)
        self.x = Widget(10, 10, 40, 40)
        self.y = Widget(30, 20, 30, 20, parent=self.x)
        self.x.move(x=100, y=100)
        self.x.resize(width=200, height=150)
