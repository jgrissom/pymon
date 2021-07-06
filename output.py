# output.py

import uasyncio as asyncio

class Output():
    def __init__(self, pin):
        self.pin = pin
    def on(self):
        self.pin.on()
    def off(self):
        self.pin.off()
    def toggle(self):
        self.pin.value(not self.pin.value())
    def flicker(self, delay):
        from time import sleep
        self.pin.on()
        sleep(delay)
        self.pin.off()        
    async def async_flicker(self, delay):
        self.pin.on()
        await asyncio.sleep(delay)
        self.pin.off()
    async def async_blink(self, delay, end_count=0):
        count = 0
        while True:
            if end_count > 0:
                count += 1
                if count > end_count:
                    break
            self.pin.on()
            await asyncio.sleep(delay)
            self.pin.off()
            await asyncio.sleep(delay)
    