from display import TFT

# ---------- Human Machine Interface Event ----------


class HMIEvent(object):
    """A Human-Machine Interface event."""
    ENCODER = 1
    LEFT_BUTTON = 2
    RIGHT_BUTTON = 3

    def __init__(self, device, value: int):
        """Create a new event.

        Args:
            device (ENCODER/LEFT_BUTTON/RIGHT_BUTTON): The device that originated this event.
            value (int): The value of the event (0/1 for button, delta for encoder).
        """
        self.device = device
        self.value = value

# ---------- Global widget managing class ----------


class WidgetDrawer(object):
    """The global widget manager."""
    _tft = None
    _width = None
    _height = None
    leftButtonFocusedWidget = None
    rightButtonFocusedWidget = None
    encoderFocusedWidget = None

    @staticmethod
    def leftButtonEvent(value: int):
        """Generates a left button event.

        Args:
            value (int): 1 for pressed, 0 for released.
        """
        if WidgetDrawer.leftButtonFocusedWidget is Widget:
            WidgetDrawer.leftButtonFocusedWidget.event(
                HMIEvent(HMIEvent.LEFT_BUTTON, value))

    @staticmethod
    def rightButtonEvent(value):
        """Generates a right button event.

        Args:
            value (int): 1 for pressed, 0 for released.
        """
        if WidgetDrawer.rightButtonFocusedWidget is Widget:
            WidgetDrawer.rightButtonFocusedWidget.event(
                HMIEvent(HMIEvent.RIGHT_BUTTON, value))

    @staticmethod
    def encoderEvent(delta: int):
        """Generates an encode event.

        Args:
            delta (int): The delta from the last event.
        """
        if WidgetDrawer.encoderFocusedWidget is Widget:
            WidgetDrawer.encoderFocusedWidget.event(
                HMIEvent(HMIEvent.ENCODER, delta))

    @staticmethod
    def init(tft: TFT):
        """Initializes the widget manager on the specified screen.

        Args:
            tft (TFT): The screen on which to start the manager.
        """
        WidgetDrawer._tft = tft
        WidgetDrawer._width, WidgetDrawer._height = tft.screensize()

    @staticmethod
    def getTFT() -> TFT:
        """Gets the global display.

        Returns:
            TFT: The display.
        """
        return WidgetDrawer._tft

    @staticmethod
    def getHeight() -> int:
        """Gets the global display's height.

        Returns:
            int: Height.
        """
        return WidgetDrawer._height

    @staticmethod
    def getWidth() -> int:
        """Gets the global display's width.

        Returns:
            int: Width.
        """
        return WidgetDrawer._width

# ---------- Widget alignment class ----------


class Alignment(object):
    """A widget alignment class."""
    LEFT_OUT = TOP_OUT = 0
    LEFT_IN = TOP_IN = 1
    CENTER = 2
    RIGHT_IN = BOTTOM_IN = 3
    RIGHT_OUT = BOTTOM_OUT = 4

    def __init__(self, horizontal=2, vertical=2):
        """Creates a new alignment.

        Args:
            horizontal (LEFT_OUT/LEFT_IN/CENTER/RIGHT_IN/RIGHT_OUT, optional): The kind of horizontal alignment. Defaults to 2.
            vertical (TOP_OUT/TOP_IN/CENTER/BOTTOM_IN/BOTTOM_OUT, optional): The kind of vertical alignment. Defaults to 2.
        """
        self.hor = horizontal
        self.ver = vertical

# ---------- Widget class ----------


class Widget(object):
    """A generic widget."""

    def __init__(self, x: int, y: int, width: int, height: int, display: TFT = None, parent: Widget = None):
        """Creates a new widget.

        Args:
            x (int): The x-coordinate of the top left corner.
            y (int): The y-coordinate of the top left corner.
            width (int): The width of the bounding box.
            height (int): The height of the bounding box.
            display (TFT, optional): The display to use. Defaults to the primary display.
            parent (Widget, optional): The parent widget. Defaults to None.
        """
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

    # ---------- Properties ----------

    # ----- x property -----

    def __get_x(self):
        return self._x

    def __set_x(self, x):
        self.move(x=x)

    x = property(__get_x, __set_x)

    # ----- y property -----

    def __get_y(self):
        return self._y

    def __set_y(self, y):
        self.move(y=y)

    y = property(__get_y, __set_y)

    # ----- width property -----

    def __get_width(self):
        return self._width

    def __set_width(self, width):
        self.resize(width=width)

    width = property(__get_width, __set_width)

    # ----- height property -----

    def __get_height(self):
        return self._height

    def __set_height(self, height):
        self.resize(height=height)

    height = property(__get_height, __set_height)

    # ---------- Functions ----------

    def __add_parent(self, parent: Widget):
        """Adds parent info to this widget and adjusts the absolute coordinates. Redraws the widget tree.

        Args:
            parent (Widget): The parent.
        """
        if parent._absolute_x is not None:
            self._absolute_x = self._x + parent._absolute_x
        if parent._absolute_y is not None:
            self._absolute_y = self._y + parent._absolute_y
        self._parent = parent
        parent._children.append(self)
        parent.drawTree()

    def addChild(self, child: Widget):
        """Adds a child to this widget.

        Args:
            child (Widget): The child.
        """
        self._children.append(child)
        child.__add_parent(self)

    def align(self, alignment: Alignment = None):
        """Aligns this widget inside its parent (which can be the screen itself).

        Args:
            alignment (Alignment, optional): The alignment. Defaults to center.
        """
        if alignment is None:
            alignment = Alignment()

        parentSize = (self._parent._width,
                      self._parent._height) or self._display.screenSize()
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

        self.move(int(newx), int(newy))

    def updateAbsolutes(self, delta_x:int, delta_y:int):
        """Updates the absolute coordinates for this widget and its descendants.

        Args:
            delta_x (int): The variation in x to be applied.
            delta_y (int): The variation in y to be applied.
        """
        self._absolute_x += delta_x
        self._absolute_y += delta_y
        for child in self._children:
            child.updateAbsolutes(delta_x, delta_y)

    def resize(self, width:int=None, height:int=None):
        """Resizes this widget.

        Args:
            width (int, optional): the new width. Defaults to None.
            height (int, optional): the new height. Defaults to None.
        """
        self._height = height or self.height
        self._width = width or self.width
        print("Resizing", self, "to", (self._height, self._width))
        self.drawTree()

    def move(self, x:int=None, y:int=None):
        """Moves this widget to new coordinates.

        Args:
            x (int, optional): The new x-coordinate. Defaults to None.
            y (int, optional): The new y-coordinate. Defaults to None.
        """
        delta_x = x - self._x if x is not None else 0
        delta_y = y - self._y if y is not None else 0
        self.updateAbsolutes(delta_x, delta_y)
        self._x += delta_x
        self._y += delta_y
        print("Moving", self, "to", (self._x, self._y))
        self.drawTree()

    def pointerEvent(self, x: int, y: int, event: HMIEvent):
        """If the coordinates of the event are inside this object's bounding box, sends the event to this widget.

        Args:
            x (int): x-coordinate of the event.
            y (int): y-coordinate of the event.
            event (HMIEvent): The event.
        """
        # Checks if the event happened inside the bounding box
        pass

    def event(self, event: HMIEvent):
        """Sends an event to this widget.

        Args:
            event (HMIEvent): The event.
        """
        pass

    def removeChild(self, child: Widget):
        """Removes a child from the children list and redraws the widget tree.

        Args:
            child (Widget): The child to be removed.
        """
        self._children.remove(child)
        self.drawTree()

    def drawChildren(self):
        if self._parent is not None:
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
        """Redraws the widget tree."""
        if self._parent is not None:
            self._parent.drawTree()
        else:
            self._display.clear()
            self.draw()
            self._display.savewin()
            self.drawChildren()
            self._display.restorewin()

    def draw(self):
        """Draws this widget."""
        # TEST DRAW
        print("Drawing", __name__, "at", (self._x, self._y, self._width,
                                          self._height), "in window of size", self._display.winsize())
        self._display.rect(self._x, self._y, self._width,
                           self._height, TFT.GREEN)
