# main.py
import machine
import micropython
from tkos import TKOS

micropython.alloc_emergency_exception_buf(100)

machine.freq(240)

os = TKOS()
os.start()

