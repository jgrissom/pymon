import uasyncio as asyncio
from async_switch import Switch
from machine import Pin, PWM
from output import Output
from time import sleep
from random import randint

# define globals
READY = 0
ACTIVE = 1
BUSY = 2
GREEN = 1
PWM_DUTY = 10

class Pymon():
    def __init__(self):
        self.btns = [ Switch( Pin(18, Pin.IN, Pin.PULL_UP) ), Switch( Pin(5, Pin.IN, Pin.PULL_UP) ), Switch( Pin(22, Pin.IN, Pin.PULL_UP) ), Switch( Pin(21, Pin.IN, Pin.PULL_UP) ) ]
        self.leds = [ Output( Pin(26, Pin.OUT) ), Output( Pin(27, Pin.OUT) ), Output( Pin(15, Pin.OUT) ), Output( Pin(14, Pin.OUT) ) ]
        for led in self.leds:
            led.off()
        # init PWM (freq = 0, duty = 0)
        self.pwm = PWM(Pin(25, Pin.OUT))
        self.pwm.duty(0)
        # red: A (4th octave), green: E (3rd octave), blue: E (4th octave), yellow: C# (4th octave)
        self.notes = [440, 165, 330, 277]
        self.status = BUSY
    def reset(self):
        self.leds[GREEN].on()
        self.status = READY
    def start(self):
        self.status = BUSY
        self.leds[GREEN].off()
        self.machine = []
        self.player = []
        sleep(.5)
        self.iterate()
    def iterate(self):
        self.status = BUSY
        self.machine.append(randint(0, 3))
        print(self.machine)
        for i in range(len(self.machine)):
            self.flicker(self.machine[i])
            sleep(.2)
        self.status = ACTIVE
    def flicker(self, idx):
        self.pwm.freq(self.notes[idx])
        self.pwm.duty(PWM_DUTY)
        self.leds[idx].on()
        sleep(.2)
        self.leds[idx].off()
        self.pwm.duty(0)
        sleep(.01)
    def verify(self, idx):
        self.status = BUSY
        self.player.append(idx)
        self.flicker(idx)
        # compare the player and machine lists
        if self.player == self.machine[0:len(self.player)]:
            if len(self.player) == len(self.machine):
                print('round completed')
                # reset player list
                self.player = []
                sleep(.8)
                self.iterate()
            self.status = ACTIVE
        else:
            print('GAME OVER')
            # turn leds on
            for led in self.leds:
                led.on()
            sleep(.2)
            # play pwm sound
            self.pwm.freq(123)
            self.pwm.duty(PWM_DUTY)
            sleep(.5)
            self.pwm.duty(0)
            # turn leds off
            for led in self.leds:
                led.off()
            self.reset()     
def press_button(idx):
    if pymon.status == ACTIVE:
        print(idx)
        pymon.verify(idx)
    elif pymon.status == READY and idx == GREEN:
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
        for led in pymon.leds:
            led.off()
        pymon.pwm.duty(0)
        pymon.pwm.deinit()
