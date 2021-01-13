# main.py
import machine
import micropython

import lvgl as lv
import lvesp32

micropython.alloc_emergency_exception_buf(100)

machine.freq(240000000)

# Import ILI9341 driver and initialized it
from ili9XXX import ili9488
disp = ili9488(factor=16)



