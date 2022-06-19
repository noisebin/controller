from gpiozero import Button
from signal import pause
import time

BSensor = Button(5) #, bounce_time=0.3)  # debounce isolation for 300 msec

# BSensor.when_line = lambda: print('Waiting for container')
# BSensor.when_no_line = lambda: print('Container detected')

def switch_on():
    print('Container detected')

def switch_off():
    print('Waiting for a container ...')

BSensor.when_pressed = switch_on
BSensor.when_released = switch_off

# pause()

while(True):
    time.sleep(0.1)
