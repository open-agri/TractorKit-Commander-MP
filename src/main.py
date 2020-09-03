# main.py

import micropython
micropython.alloc_emergency_exception_buf(100)

import machine
machine.freq(240)

from tkos import TKOS

os = TKOS()
os.start()

