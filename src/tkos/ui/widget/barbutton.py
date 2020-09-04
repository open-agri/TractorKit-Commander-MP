from display import TFT
from tkos.ui.widget.rectangle import Rectangle
from tkos.ui.widget.padding import Padding

class BarButton(Rectangle):
    def __init__(self, x, y, width=None, height=None, display=None, parent=None, bgcolor=TFT.ORANGE, padding=None, text=None):
        if text is str and width is None:
            hor_pad = 0
            if padding is Padding:
                hor_pad = padding.l + padding.r
            width = TFT.textWidth + hor_pad
        
        if text is str and height is None:
            ver_pad = 0
            if padding is Padding:
                ver_pad = padding.t + padding.b
            height = TFT.fontSize + ver_pad

            ## STOP!!! First create label widget, then proceed to create this one.
            ## Try string height/width detection by drawing a bounding box
        super().__init__(x, y, width, height, display, parent, bgcolor)