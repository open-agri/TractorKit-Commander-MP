from display import TFT

class WidgetDrawer(object):
    _tft = None
    _width = None
    _height = None

    @staticmethod
    def init(tft, width, height):
        WidgetDrawer._tft = tft
        WidgetDrawer._width = width
        WidgetDrawer._height = height
    
    @staticmethod
    def getTFT():
        return WidgetDrawer._tft

    @staticmethod
    def getHeight():
        return WidgetDrawer._height

    @staticmethod
    def getWidth():
        return WidgetDrawer._width



class Widget(object):
    def __init__(self, x, y, width, height, display = None, parent = None):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._display = WidgetDrawer.getTFT() if (display is None) else display
        self._children = []
        self._parent = None

        if(parent is not None):
            if(parent._absolute_x is not None):
                self._absolute_x = self._x + parent._absolute_x
            
            if(parent._absolute_y is not None):
                self._absolute_y = self._y + parent._absolute_y

            parent._children.append(self)
            parent.__drawTree()
        else:
            self._absolute_x = self._x
            self._absolute_y = self._y
            self.__draw()

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __updateAbsolutes(self, delta_x, delta_y):
        self._absolute_x += delta_x
        self._absolute_y += delta_y
        for child in self._children:
            child.__updateAbsolutes(delta_x, delta_y)

    def resize(self, height = None, width = None):
        self._height = height or self.height
        self._width = width or self.width
        self.__drawTree()
        print("Resized", __name__, "to", (self._height, self._width))

    def move(self, x = None, y = None):
        delta_x = x - self._x if x is not None else 0
        delta_y = y - self._y if y is not None else 0
        self.__updateAbsolutes(delta_x, delta_y)
        self._x += delta_x
        self._y += delta_y
        self.__drawTree()
        print("Moved", __name__, "by", (delta_x, delta_y))

    def pointerEvent(self):
        pass

    def removeChild(self, child):
        self._children.remove(child)
        self.__drawTree()

    def __drawChildren(self):
        if(self._parent is not None):
            winwidth = self._parent._width - self._x if self._x + self._width > self._parent._width else self._width
            winheight = self._parent._height - self._y if self._y + self._height > self._parent._height else self._height
        else:
            winwidth = WidgetDrawer.getWidth() - self._x if self._x + self._width > WidgetDrawer.getWidth() else self._width
            winheight = WidgetDrawer.getHeight() - self._y if self._y + self._height > WidgetDrawer.getHeight() else self._height

        self._display.setwin(self._absolute_x, self._absolute_y, self._x + winwidth- 1, self._y + winheight - 1)
        for child in self._children:
            child.__draw()
            child.__drawChildren()

    def __drawTree(self):
        if(self._parent is not None):
            self._parent.drawTree()
        else:
            self._display.clear()
            self.__draw()
            self._display.savewin()
            self.__drawChildren()
            self._display.restorewin()


    def __draw(self):
        ## TEST DRAW
        print("Drawing", __name__, "at", (self._x, self._y, self._width, self._height), "in", self._display.winsize())
        self._display.line(self._x, self._y, self._x + self._width - 1, self._y + self._height - 1, TFT.GREEN)
        self._display.line(self._x, self._y + self._height - 1, self._x + self._width - 1, self._y, TFT.GREEN)
        self._display.rect(self._x, self._y, self._width, self._height, TFT.GREEN)