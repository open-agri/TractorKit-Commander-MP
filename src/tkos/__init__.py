from display import TFT
import tkos.drivers as drivers
from tkos.drivers.rotary_esp32 import RotaryIRQ
from tkos.ui import UI

class TKOS:
    """The base class of the operating system."""
    display_width = 480
    display_height = 320
    def __init__(self):
        """Initialize an instance of the OS."""
        print('Initializing tkos...')
        self.tft = None
        self.gui = None
        self.encoder = None

    def start(self):
        """Start this instance of the OS."""
        print('Welcome to tkos')
        self.init_display()
        self.init_gui(self.tft)
        self.init_encoder()

    def init_display(self):
        """Initialize the display driver."""
        print('Initializing TFT...')
        self.tft = TFT()

        self.tft.init(self.tft.ILI9488, mosi=13, miso=35, clk=14, cs=15, dc=2, speed=40000000,
                width=self.display_width, height=self.display_height, rst_pin=4, backl_pin=27, backl_on=1,
                rot=self.tft.LANDSCAPE_FLIP, bgr=True, splash=False)

    def init_encoder(self):
        """Initialize the encoder driver."""
        self.encoder = RotaryIRQ(25, 26, range_mode=drivers.Rotary.RANGE_UNBOUNDED)

    def init_gui(self, tft:TFT):
        """Initializes the user interface on the specified display.

        Args:
            tft (TFT): The display.
        """
        self.gui = UI(tft)
