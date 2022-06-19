#!/usr/bin/env python3

#  TODO: In the middle of updating to lgpio ABI as necessary for Ubuntu - work in progress

# Script simply waits on input changes from the bottle deteector (laser/LDR sensor)
# and reports those changes.

# import RPi.GPIO as GPIO
import lgpio
from gpiozero import LineSensor
import datetime
import time
from time import sleep
# import logging # not necessary yet?

# TODO: could remove all mentions of GPIO by employing the equivalent gpiozero functions instead
# GPIO.setwarnings(False)
# GPIO.cleanup()
# GPIO.setmode(GPIO.BCM)                 #  Set GPIO pin numbering

# lgpio.setwarnings(False)
# lgpio.cleanup()
lgpio.setmode(lgpio.BCM)                 #  Set lgpio pin numbering

ContSensor = LineSensor(5)            # laser>LDR>Opto input pin
ContSensor.when_line = lambda: print('Waiting for container ...')
ContSensor.when_no_line = lambda: print('Container detected at ',datetime.datetime.now())

while True:
    time.sleep(0.1)                    #  Delay of 0.1 seconds between checks on the input pin

