import uasyncio as asyncio
from async_switch import Switch
from machine import Pin

class Pymon():
    def __init__(self):
        self.btns = [ Switch( Pin(18, Pin.IN, Pin.PULL_UP) ), Switch( Pin(5, Pin.IN, Pin.PULL_UP) ), Switch( Pin(22, Pin.IN, Pin.PULL_UP) ), Switch( Pin(21, Pin.IN, Pin.PULL_UP) ) ] 
        
def press_button(idx):
    print(idx)

async def main():
    for i in range(len(pymon.btns)):
        pymon.btns[i].open_func(press_button, (i,))
    
    while True:
        await asyncio.sleep(.01)

if __name__ == '__main__':
    try:      
        pymon = Pymon()
        asyncio.run(main())
    finally:
        print("goodbye")
