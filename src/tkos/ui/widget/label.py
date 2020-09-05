from display import TFT
from tkos.ui.widget import Widget, WidgetDrawer

class Label(Widget):
    """A text label."""
    def __init__(self, x:int, y:int, display:TFT=None, parent:Widget=None, font=TFT.FONT_DejaVu18, text:str=None, color=TFT.WHITE):
        """Creates a new label.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            display (TFT, optional): The display. Defaults to the main display.
            parent (Widget, optional): The parent widget. Defaults to None.
            font (int, optional): The font to use on this text. Defaults to TFT.FONT_DejaVu18.
            text (str, optional): The contents of the label. Defaults to None.
            color (int, optional): The color of the text. Defaults to TFT.WHITE.
        """
        self._font = font
        self._text = text or ''
        self._color = color

        size = self.__compute_size()
        super().__init__(x, y, size[0], size[1], display, parent, fillsBox=False)

    # ---------- Properties ----------

    # ----- Text property -----

    def __get_text(self):
        return self._text

    def __set_text(self, text):
        self._text = text or ""
        size = self.__compute_size()
        self.__resize(width=size[0], height=size[1])

    text = property(__get_text, __set_text)

    # ----- Font property -----

    def __get_font(self):
        return self._font

    def __set_font(self, font):
        self._font = font
        self.drawTree()

    font = property(__get_font, __set_font)

    # ----- Color property -----

    def __get_color(self):
        return self._color

    def __set_color(self, color):
        self._color = color
        self.drawTree()

    # ---------- Functions ----------

    def __compute_size(self):
        """Calculates the size of this label based on font size, length and lines.

        Returns:
            (int, int): Width and height of the label.
        """
        WidgetDrawer.getTFT().font(self._font, transparent=True)
        tokens = self._text.split('\n')
        lines = len(tokens)
        width = 0
        for token in tokens:
            t_width = WidgetDrawer.getTFT().textWidth(token)
            if t_width > width:
                width = t_width

        return (width, WidgetDrawer.getTFT().fontSize()[1] * lines)

    def draw(self):
        """Draws the widget."""
        print("Drawing", self, "at", (self.x, self.y, self.width, self.height), "in window of size", self._display.winsize())
        self._display.font(self._font, transparent=True)
        self._display.text(self.x, self.y, self._text, color=self._color)
