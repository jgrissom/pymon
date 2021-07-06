import uasyncio as asyncio
from async_switch import Switch
from machine import Pin
from output import Output

# define globals
READY = 0
ACTIVE = 1
BUSY = 2
GREEN = 1

class Pymon():
    def __init__(self):
        self.btns = [ Switch( Pin(18, Pin.IN, Pin.PULL_UP) ), Switch( Pin(5, Pin.IN, Pin.PULL_UP) ), Switch( Pin(22, Pin.IN, Pin.PULL_UP) ), Switch( Pin(21, Pin.IN, Pin.PULL_UP) ) ]
        self.leds = [ Output( Pin(26, Pin.OUT) ), Output( Pin(27, Pin.OUT) ), Output( Pin(15, Pin.OUT) ), Output( Pin(14, Pin.OUT) ) ]
        for led in self.leds:
            led.off()
            
        self.status = BUSY
    def reset(self):
        self.leds[GREEN].on()
        self.status = READY
    def start(self):
        self.status = BUSY
        self.leds[GREEN].off()
        
def press_button(idx):
    if pymon.status == READY and idx == GREEN:
        print('start game')
        pymon.start()

async def main():
    for i in range(len(pymon.btns)):
        pymon.btns[i].open_func(press_button, (i,))
    
    pymon.reset()
    while True:
        await asyncio.sleep(.01)

if __name__ == '__main__':
    try:     
        pymon = Pymon()
        asyncio.run(main())
    finally:
        print("goodbye")
