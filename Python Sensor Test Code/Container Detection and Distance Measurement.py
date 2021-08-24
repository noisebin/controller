#  Ref: http://www.d3noob.org/2018/04/this-post-is-part-of-book-raspberry-pi.html


#  !/usr/bin/python
#  encoding:utf-8

import RPi.GPIO as GPIO                    #  Import GPIO library
import time  #  Import time library
import subprocess # Used for creating a separate process for playing a sound
from gpiozero import LineSensor
from signal import pause
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)                     #  Set GPIO pin numbering

TRIG = 18                                  #  Associate pin 15 to TRIG
ECHO = 24                                  #  Associate pin 14 to Echo

ContSensor = LineSensor(21)# Opto output
ContSensor.when_line = lambda: print('Waiting for container')
ContSensor.when_no_line = lambda: subprocess.Popen(['aplay', '/home/pi/Desktop/samples/loop_safari.wav'])

print("Distance measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)                  #  Set pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)                   #  Set pin as GPIO in

current_distance = -1.0
previous_distance = -1.0
INNER_BOUND = 20
OUTER_BOUND = 100
pulse_start = 0.0

while True:
    GPIO.output(TRIG, False)                 #  Set TRIG as LOW
    #print("Waiting For Sensor To Settle")
    time.sleep(0.01)                         #  Delay of 0.01 seconds

    GPIO.output(TRIG, True)                  #  Set TRIG as HIGH
    time.sleep(0.00001)                      #  Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #  Set TRIG as LOW

    while GPIO.input(ECHO) == 0:               #  Check if Echo is LOW
        pulse_start = time.time()              #  Time of the last  LOW pulse

    while GPIO.input(ECHO) == 1:               #  Check whether Echo is HIGH
        pulse_end = time.time()                #  Time of the last HIGH pulse

        pulse_duration = pulse_end - pulse_start  #  pulse duration to a variable

    current_distance = pulse_duration * 17150        #Calculate distance
    current_distance = round(current_distance, 2)    #Round to two decimal points

    # If the most recent pair of distances show a pattern of moving from outside to inside the 'detection zone'
    if((current_distance > INNER_BOUND and current_distance < OUTER_BOUND) and
       (previous_distance <= INNER_BOUND or previous_distance >= OUTER_BOUND)):
        # play a sound in a separate process
        process = subprocess.Popen(['aplay', '/home/pi/Desktop/samples/loop_amen.wav'])
        process.wait()

    previous_distance = current_distance
