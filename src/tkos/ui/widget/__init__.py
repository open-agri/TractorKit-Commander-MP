from display import TFT

class WidgetDrawer(object):
    _tft = None
    
    @staticmethod
    def init(tft):
        WidgetDrawer._tft = tft
    
    @staticmethod
    def getTFT():
        return WidgetDrawer._tft

class Widget(object):
    def __init__(self, x, y, width, height, display = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = WidgetDrawer.getTFT() if (display is None) else display

    def draw(self):
        self.display.line(self.x, self.y, self.x + self.width - 1, self.y + self.height - 1, TFT.GREEN)
        self.display.line(self.x, self.y + self.height - 1, self.x + self.width - 1, self.y, TFT.GREEN)
        self.display.rect(self.x, self.y, self.width, self.height, TFT.GREEN)
