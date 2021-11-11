from gpiozero import LineSensor
from signal import pause
# using Laser (Jaycar XC-4490) and LDR (XC-4446)
# LDR "No Light' = LOW (1.79Vdc)
# LDR 'Container sensed' = HIGH (4.2 - 5.0Vdc)
ContSensor = LineSensor(21)# Opto output
ContSensor.when_line = lambda: print('Waiting for container')
ContSensor.when_no_line = lambda: print('Container detected')
pause()