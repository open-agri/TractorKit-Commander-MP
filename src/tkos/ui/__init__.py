from tkos.ui.widget import Widget
from tkos.ui.widget import WidgetDrawer

class UI:
    def __init__(self, tft):
        WidgetDrawer.init(tft)


        # test
        x = Widget(40, 40, 40, 40)
        y = Widget(30, 20, 30, 20)
        x.addChild(y)
        x.draw()
