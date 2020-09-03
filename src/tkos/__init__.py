import display
import tkos.drivers as drivers
from tkos.drivers.rotary_esp32 import RotaryIRQ
from tkos.ui import UI

class TKOS:
    def __init__(self):
        print('Initializing tkos...')
        self.tft = None
        self.gui = None

    def start(self):
        print('Welcome to tkos')
        self.init_display()
        self.init_encoder()
        self.init_gui(self.tft)

    def init_display(self):
        print('Initializing TFT...')
        self.tft = display.TFT()

        self.tft.init(self.tft.ILI9488, mosi=13, miso=35, clk=14, cs=15, dc=2, speed=40000000,
                width=480, height=320, rst_pin=4, backl_pin=27, backl_on=1,
                rot=self.tft.LANDSCAPE_FLIP, bgr=True, splash=False)
    
    def init_encoder(self):
        self.encoder = RotaryIRQ(25, 26, range_mode=drivers.Rotary.RANGE_UNBOUNDED)

    def init_gui(self, tft):
        self.gui = UI(tft)
