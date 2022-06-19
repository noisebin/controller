from gpiozero import LineSensor
from signal import pause
import time

# using Laser (Jaycar XC-4490) and LDR (XC-4446)
# LDR "No Light' = LOW (1.79Vdc)
# LDR 'Container sensed' = HIGH (4.2 - 5.0Vdc)

ContSensor = LineSensor(6)

# ContSensor.when_line = lambda: print('Waiting for container')
# ContSensor.when_no_line = lambda: print('Container detected')

def switch_on():
    print('Container detected')
#    print(f"GPIO6 is: %d",ContSensor.value())
#    time.sleep(0.3)

def switch_off():
    print('Waiting for a container ...')
#    print(f"GPIO6 is: %d",ContSensor.value())
#    time.sleep(0.3)

ContSensor.when_no_line = switch_on
ContSensor.when_line = switch_off

while(True):
    time.sleep(0.1)
