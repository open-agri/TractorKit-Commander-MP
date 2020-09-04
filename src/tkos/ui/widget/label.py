from display import TFT
from tkos.ui.widget import Widget, WidgetDrawer

class Label(Widget):
    def __init__(self, x, y, display=None, parent=None, font=TFT.FONT_DejaVu18, text=None, color=TFT.WHITE):
        self._font = font
        self._text = text or ""
        self._color = color

        size = self.__compute_size()
        super().__init__(x, y, size[0], size[1], display, parent)

    def __compute_size(self):
        WidgetDrawer.getTFT().font(self._font, transparent=True)
        tokens = self._text.split('\n')
        lines = len(tokens)
        width = 0
        for token in tokens:
            t_width = WidgetDrawer.getTFT().textWidth(token)
            if t_width > width:
                width = t_width

        return (width, WidgetDrawer.getTFT().fontSize()[1] * lines)

    def __get_text(self):
        return self._text

    def __set_text(self, text):
        self._text = text or ""
        size = self.__compute_size()
        self.resize(width=size[0], height=size[1])

    text = property(__get_text, __set_text)

    # TODO: Implement color and font get/set


    def draw(self):
        print("Drawing", __name__, "at", (self._x, self._y, self._width, self._height), "in window of size", self._display.winsize())
        self._display.font(self._font, transparent=True)
        self._display.text(self._x, self._y, self._text, color=self._color)
