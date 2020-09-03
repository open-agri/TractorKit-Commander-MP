from machine import Pin
from tkos.drivers import Rotary
from sys import platform

class RotaryIRQ(Rotary): 
    
    def __init__(self, pin_num_clk, pin_num_dt, min_val=0, max_val=10, reverse=False, range_mode=Rotary.RANGE_UNBOUNDED):
        
        super().__init__(min_val, max_val, reverse, range_mode, pin_num_clk, pin_num_dt)
        self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_DOWN, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._process_rotary_pins)
        self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_DOWN, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._process_rotary_pins)
        
    def _disable_clk_irq(self):
        self._pin_clk.init(handler=None)
        
    def _disable_dt_irq(self):
        self._pin_dt.init(handler=None)     
    
    def _hal_get_clk_value(self):
        return self._pin_clk.irqvalue()
        
    def _hal_get_dt_value(self):
        return self._pin_dt.irqvalue()   
    
    def _hal_enable_irq(self):
        self._pin_clk.init(handler=self._process_rotary_pins)
        self._pin_clk.init(handler=self._process_rotary_pins)

    def _hal_disable_irq(self): 
        self._disable_clk_irq()
        self._disable_dt_irq()     

    def _hal_close(self):
        self._hal_disable_irq()