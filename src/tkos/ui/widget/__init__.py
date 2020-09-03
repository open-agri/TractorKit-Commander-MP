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
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._display = WidgetDrawer.getTFT() if (display is None) else display
        self._children = []
        self._parent = None

        self.draw()

    def pointerEvent(self):
        pass

    def addChild(self, child):
        self._children.append(child)
        self.draw()

    def removeChild(self, child):
        self._children.remove(child)
        self.draw()

    def drawChildren(self):
        self._display.savewin()
        self._display.setwin(self._x, self._y, self._x + self._width - 1, self._y + self._height - 1)
        for child in self._children:
            # TODO: Set starting coordinates
            child.draw()

        self._display.restorewin()

    def draw(self):
        ## TEST DRAW
        self._display.line(self._x, self._y, self._x + self._width - 1, self._y + self._height - 1, TFT.GREEN)
        self._display.line(self._x, self._y + self._height - 1, self._x + self._width - 1, self._y, TFT.GREEN)
        self._display.rect(self._x, self._y, self._width, self._height, TFT.GREEN)

        self.drawChildren()
