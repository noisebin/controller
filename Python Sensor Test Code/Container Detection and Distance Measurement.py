#!/usr/bin/env python3

#  Ref: http://www.d3noob.org/2018/04/this-post-is-part-of-book-raspberry-pi.html

#  !/usr/bin/python
#  encoding:utf-8

import sys
import RPi.GPIO as GPIO                    #  Import GPIO library
import time  #  Import time library
import subprocess # Used for creating a separate process for playing a sound
from gpiozero import LineSensor
from signal import pause
from multi import Player
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)                           #  Set GPIO pin numbering

TRIG = 18                                        #  Associate pin 15 to TRIG
ECHO = 24                                        #  Associate pin 14 to Echo
scaling = 17150                                  #  Distance / echo time conversion and scaling factor

ContSensor = LineSensor(21)                      #  Opto output seen on pin 21 (?)
ContSensor.when_line = lambda: print('Waiting for container')
ContSensor.when_no_line = lambda: subprocess.Popen(['aplay', 'samples/loop_safari.wav'])

def display_begin():
    sys.stdout.write("\u001b[1;1H")                  #  start at a consistent position in window
    sys.stdout.write("\u001b[0J")                    #  clear from cursor to bottom of screen
    sys.stdout.write("\u001b[38;5;121m")             #  ESC[38;5;⟨n⟩m Select foreground color
    sys.stdout.write("\u001b[45m")                   #  ESC[45m Select background color

    print("====== NoiseBin Mark 1 Human Detector =======")
    sys.stdout.write("\u001b[0m")                    # ESC[39;m reset to default fore/background colors

    print()
    print("Distance measurement in progress")

def display_detection(status):
    sys.stdout.write("\u001b[13;1H")
    sys.stdout.write("\u001b[0K")                #  Clear to end of line
    print("Status: ", status)

def display_measured(measured):
    sys.stdout.write("\u001b[15;1H")
    sys.stdout.write("\u001b[0K")                #  Clear to end of line
    print(measured)
    # sys.stdout.write("Status: ")                 #  -
    


GPIO.setup(TRIG, GPIO.OUT)                       #  Set trigger pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)                        #  Set response pin as GPIO in

current_distance = -1.0
previous_distance = -1.0
INNER_BOUND = 20
OUTER_BOUND = 200

display_begin()

player = Player('samples/')
while True:
    GPIO.output(TRIG, False)                     #  Set TRIG as LOW
    # print("Waiting For Sensor To Settle")
    time.sleep(0.3)                              #  Delay of 0.1 seconds

    # Send a trigger pulse
    GPIO.output(TRIG, True)                      #  Set TRIG as HIGH
    time.sleep(0.00001)                          #  Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                     #  Set TRIG as LOW

    while GPIO.input(ECHO) == 0:                 #  Check if Echo is LOW
        pulse_start = time.time()                #  Time of the last  LOW pulse

    while GPIO.input(ECHO) == 1:                 #  Check whether Echo is HIGH
        pulse_end = time.time()                  #  Time of the last HIGH pulse

    pulse_duration = pulse_end - pulse_start

    current_distance = pulse_duration * scaling  #  Calculate distance
    current_distance = round(current_distance, 2)#  Round to two decimal points

    sys.stdout.write("\u001b[13;1H")             #  start at a consistent position in window
    # sys.stdout.write("\u001b[0J")                #  clear from cursor to bottom of screen
    

    # If the most recent pair of distances show a pattern of moving from outside to inside the 'detection zone'
    if((current_distance > INNER_BOUND and current_distance < OUTER_BOUND) and
       (previous_distance <= INNER_BOUND or previous_distance >= OUTER_BOUND)):
        # play a sound in a separate process
        player.play()
        display_detection("Moving into the detection zone")
        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
        # measured = "Previous distance: " + previous_distance + " Current distance: " + current_distance
        display_measured(measured)

    # If the most recent pair of distances show a pattern of moving from inside to outside the 'detection zone'
    elif((current_distance <= INNER_BOUND or current_distance >= OUTER_BOUND) and
         (previous_distance > INNER_BOUND and previous_distance < OUTER_BOUND)):
        # play a sound in a separate process
        #player.play()
        display_detection("Moving out of the detection zone")
        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
        display_measured(measured)

    # if motionless, or outside the monitored range
    # TODO motionless is a separate, interesting state which we should identify and treat separately
    else:
        # sys.stdout.write("\u001b[17;1H")        # start at a consistent position in window
        display_detection("No movement, or out of range")                   # echo response is out of range

    previous_distance = current_distance
