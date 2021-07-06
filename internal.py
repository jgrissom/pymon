import uasyncio as asyncio
import tinypico as TinyPICO
from micropython_dotstar import DotStar
from machine import Pin, SoftSPI

class TinyPICODotStar(DotStar):
    def __init__(self):
        # Configure SPI for controlling the DotStar
        # Internally we are using software SPI for this as the pins being used are not hardware SPI pins
        spi = SoftSPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) )
        # dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
        super().__init__(spi, 1, brightness = .5)
        TinyPICO.set_dotstar_power(True)
        self.BLACK = (0,0,0)
    def on(self, color):
        self[0] = color
    def off(self):
        self[0] = self.BLACK
    def kill(self):
        self.off()
        TinyPICO.set_dotstar_power(False) 
    def toggle(self, color):
        if self[0][0] == color[0] and self[0][1] == color[1] and self[0][2] == color[2]:
            self[0] = self.BLACK
        else:
            self[0] = color
    async def async_fade():
        b = self.brightness
        print(b)
    async def async_flicker(self, color, delay):
        self.on(color)
        await asyncio.sleep(delay)
        self.off()
    async def async_blink(self, color, delay, end_count=0):
        count = 0
        while True:
            if end_count > 0:
                count += 1
                if count > end_count:
                    break
            self.on(color)
            await asyncio.sleep(delay)
            self.off()
            await asyncio.sleep(delay)
