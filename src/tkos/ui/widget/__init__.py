from display import TFT

class HMIEvent(object):
    ENCODER = 1
    LEFT_BUTTON = 2
    RIGHT_BUTTON = 3

    def __init__(self, device, value):
        self.device = device
        self.value = value


class WidgetDrawer(object):
    _tft = None
    _width = None
    _height = None
    leftButtonFocusedWidget = None
    rightButtonFocusedWidget = None
    encoderFocusedWidget = None

    @staticmethod
    def leftButtonEvent(value):
        if WidgetDrawer.leftButtonFocusedWidget is Widget:
            WidgetDrawer.leftButtonFocusedWidget.event(
                HMIEvent(HMIEvent.LEFT_BUTTON, value))

    @staticmethod
    def rightButtonEvent(value):
        if WidgetDrawer.rightButtonFocusedWidget is Widget:
            WidgetDrawer.rightButtonFocusedWidget.event(
                HMIEvent(HMIEvent.RIGHT_BUTTON, value))

    @staticmethod
    def encoderEvent(delta):
        if WidgetDrawer.encoderFocusedWidget is Widget:
            WidgetDrawer.encoderFocusedWidget.event(
                HMIEvent(HMIEvent.ENCODER, delta))

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


class Alignment(object):
    LEFT_OUT = TOP_OUT = 0
    LEFT_IN = TOP_IN = 1
    CENTER = 2
    RIGHT_IN = BOTTOM_IN = 3
    RIGHT_OUT = BOTTOM_OUT = 4
    def __init__(self, horizontal=2, vertical=2):
        self.hor = horizontal
        self.ver = vertical
        

class Widget(object):
    def __init__(self, x, y, width, height, display:TFT=None, parent:Widget=None):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._display = WidgetDrawer.getTFT() if (display is None) else display
        self._children = []
        self._parent = None

        if parent is not None:
            self.__add_parent(parent)
        else:
            self._absolute_x = self._x
            self._absolute_y = self._y
            self.draw()

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

    def __add_parent(self, parent:Widget):
        if parent._absolute_x is not None:
            self._absolute_x = self._x + parent._absolute_x
        if parent._absolute_y is not None :
            self._absolute_y = self._y + parent._absolute_y
        self._parent = parent
        parent._children.append(self)
        parent.drawTree()

    def addChild(self, child:Widget):
        self._children.append(child)
        child.__add_parent(self)

    def align(self, alignment:Alignment=None):
        if alignment is None:
            alignment = Alignment()
        
        parentSize = (self._parent._width, self._parent._height) or self._display.screenSize()
        newx = self._x
        newy = self._y

        if alignment.hor == Alignment.LEFT_OUT:
            newx = -self._width
        elif alignment.hor == Alignment.LEFT_IN:
            newx = 0
        elif alignment.hor == Alignment.CENTER:
            newx = (parentSize[0] - self._width) / 2
        elif alignment.hor == Alignment.RIGHT_IN:
            newx = parentSize[0] - self._width
        elif alignment.hor == Alignment.RIGHT_OUT:
            newx = parentSize[0]

        if alignment.ver == Alignment.TOP_OUT:
            newy = -self._height
        elif alignment.ver == Alignment.TOP_IN:
            newy = 0
        elif alignment.ver == Alignment.CENTER:
            newy = (parentSize[1] - self._height) / 2
        elif alignment.ver == Alignment.BOTTOM_IN:
            newy = parentSize[1] - self._height
        elif alignment.ver == Alignment.BOTTOM_OUT:
            newy = parentSize[1]

        print("Aligning", self)
        self.move(int(newx), int(newy))

    def updateAbsolutes(self, delta_x, delta_y):
        self._absolute_x += delta_x
        self._absolute_y += delta_y
        for child in self._children:
            child.updateAbsolutes(delta_x, delta_y)

    def resize(self, height=None, width=None):
        self._height = height or self.height
        self._width = width or self.width
        print("Resizing", self, "to", (self._height, self._width))
        self.drawTree()

    def move(self, x=None, y=None):
        delta_x = x - self._x if x is not None else 0
        delta_y = y - self._y if y is not None else 0
        self.updateAbsolutes(delta_x, delta_y)
        self._x += delta_x
        self._y += delta_y
        print("Moving", self, "to", (self._x, self._y))
        self.drawTree()

    def pointerEvent(self, x:int, y:int, event:HMIEvent):
        # Checks if the event happened inside the bounding box
        pass

    def event(self, event:HMIEvent):
        pass

    def removeChild(self, child:Widget):
        self._children.remove(child)
        self.drawTree()

    def drawChildren(self):
        if self._parent is not None :
            winwidth = self._parent.width - self._x if self._x + \
                self._width > self._parent.width else self._width
            winheight = self._parent.width - self._y if self._y + \
                self._height > self._parent.width else self._height
        else:
            winwidth = WidgetDrawer.getWidth() - self._x if self._x + \
                self._width > WidgetDrawer.getWidth() else self._width
            winheight = WidgetDrawer.getHeight() - self._y if self._y + \
                self._height > WidgetDrawer.getHeight() else self._height

        self._display.setwin(self._absolute_x, self._absolute_y,
                             self._absolute_x + winwidth - 1, self._absolute_y + winheight - 1)
        for child in self._children:
            child.draw()
            child.drawChildren()

    def drawTree(self):
        if self._parent is not None:
            self._parent.drawTree()
        else:
            self._display.clear()
            self.draw()
            self._display.savewin()
            self.drawChildren()
            self._display.restorewin()

    def draw(self):
        # TEST DRAW
        print("Drawing", __name__, "at", (self._x, self._y, self._width,
                                          self._height), "in window of size", self._display.winsize())
        self._display.rect(self._x, self._y, self._width,
                           self._height, TFT.GREEN)
