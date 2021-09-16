#!/usr/bin/env python3

#  Ref: http://www.d3noob.org/2018/04/this-post-is-part-of-book-raspberry-pi.html

#  !/usr/bin/python
#  encoding:utf-8

# The import command makes separate packages of code available to use in your program
# Here we are importing some packages that give us the ability to do extra things
import sys # sys gives us access to helpful Operating System commands
import RPi.GPIO as GPIO # GPIO lets us talk to the Pi's pins
import time  # time lets us make the code 'sleep' for an amount of time

from gpiozero import LineSensor # The LineSensor package lets us use the light detecting sensor
from signal import pause # Pause lets us make the code wait at a certain point
from multi import Player # Player is the package that has the code to play sounds

# Prepare the Pi's pins for use
GPIO.setwarnings(False) # Ignore warnings
GPIO.cleanup() # Reset the state of the pins
GPIO.setmode(GPIO.BCM) #  Set GPIO pin numbering

TRIG = 18 # TRIG is a variable that here holds 18.
          # We use it to point towards pin 18 on the Pi.
          # (We want pin 18 to be where we connect the device that
          # *triggers* an ultrasound pulse).

ECHO = 24 # ECHO is a variable that here holds 24.
          # We use it to point towards pin 24 on the Pi.
          # (We want pin 24 to be where we receive an *echo* from the
          # ultrasound pulse).
scaling = 17150 #  Distance / echo time conversion and scaling factor

player = Player('samples/') # Set up the sound player and point it towards the sounds

ContSensor = LineSensor(21) #  Make the Light sensor look for a signal on pin 21
# Tell the light sensor code to print a message when the line of light is un-broken
ContSensor.when_line = lambda: print('Waiting for container')
# Tell the light sensor to play a sound when the line of light is broken
ContSensor.when_no_line = lambda: player.play()

# display_begin sets up the computer screen to display messages in various styles
# (coloured and positioned according to special codes called ANSI escape codes)
# For more details see eg. https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
def display_begin():
    sys.stdout.write("\u001b[1;1H")                  #  start at a consistent position in window
    sys.stdout.write("\u001b[0J")                    #  clear from cursor to bottom of screen
    sys.stdout.write("\u001b[38;5;121m")             #  ESC[38;5;⟨n⟩m Select foreground color
    sys.stdout.write("\u001b[45m")                   #  ESC[45m Select background color

    print("====== NoiseBin Mark 1 Human Detector =======")
    sys.stdout.write("\u001b[0m")                    # ESC[39;m reset to default fore/background colors

    print()
    print("Distance measurement in progress")

# display_detection displays messages about whether the ultrasound sensor detects anything,
# (again using ANSI escape codes to style the messages)
def display_detection(status):
    sys.stdout.write("\u001b[13;1H")
    sys.stdout.write("\u001b[0K")                #  Clear to end of line
    print("Status: ", status)

# display_measured displays messages about the distances that something was detected at,
# (again using ANSI escape codes to style the messages)
def display_measured(measured):
    sys.stdout.write("\u001b[15;1H")
    sys.stdout.write("\u001b[0K")                #  Clear to end of line
    print(measured)
    # sys.stdout.write("Status: ")                 #  -


GPIO.setup(TRIG, GPIO.OUT)                       #  Set trigger pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)                        #  Set response pin as GPIO in

# Set some variables to hold the values of the distances that something was detected at,
# last time the sensor saw something (last_distance) and when the sensor saw something *this time* (current_distance)
# We store -1 in them to start with so that the values are outside the detection zone in the very beginning
current_distance = -1.0
previous_distance = -1.0

# Set some variables to hold the values of the boundaries of the 'detection zone'.
# INNER_BOUND is the inner edge of the detection zone (edge closest to the sensor)
# OUTER_BOUND is the outer edge of the detection zone (edge furthest away from the sensor)
# Values are in cm
INNER_BOUND = 20
OUTER_BOUND = 200

# Now we call display_begin to start up the messages on the screen
display_begin()

# While True is a way of making something loop forever.
# (While will only run the code below it if the X in while X is the same value as True).
# Since the True in while True is always true, the code under the while will loop forever.
while True:
    GPIO.output(TRIG, False)                     #  Set the signal on the TRIG pin to LOW (eg. off)
    # print("Waiting For Sensor To Settle")
    time.sleep(0.1)                              #  Delay of 0.1 seconds

    # Send a trigger pulse
    GPIO.output(TRIG, True)                      #  Set the signal on the TRIG pin to HIGH (eg. on)
    time.sleep(0.00001)                          #  Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                     #  Set the signal on the TRIG pin to LOW (eg. off)

    while GPIO.input(ECHO) == 0:                 #  When the signal on the ECHO pin is LOW (eg no echo has returned right now)
        pulse_start = time.time()                #  Get the time of the last LOW pulse (just *after* the last echo returned)

    while GPIO.input(ECHO) == 1:                 #  When the signal on the ECHO pin is HIGH (eg an echo has just returned)
        pulse_end = time.time()                  #  Get the time of the last HIGH pulse (the time the echo returned)

    pulse_duration = pulse_end - pulse_start     # Work out the total time from the trigger being sent to the echo returning

    current_distance = pulse_duration * scaling  #  Calculate distance based on the total time this took
    current_distance = round(current_distance, 2)#  Round to two decimal points

    # Prepare for writing some new messages to the screen
    sys.stdout.write("\u001b[13;1H")             #  start at a consistent position in window

    # If the most recent pair of distances show a pattern of moving from outside to inside the 'detection zone'
    if((current_distance > INNER_BOUND and current_distance < OUTER_BOUND) and
       (previous_distance <= INNER_BOUND or previous_distance >= OUTER_BOUND)):
        # Play a sound in a separate thread, so that it doesn't interrupt the rest of our code
        player.play()

        # Call our message displaying functions to write messages to the screen about what has just happened
        display_detection("Moving into the detection zone")
        # f is for formatting a message comprised of multiple parts 
        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
        display_measured(measured)

    # If the most recent pair of distances show a pattern of moving from inside to outside the 'detection zone'
    elif((current_distance <= INNER_BOUND or current_distance >= OUTER_BOUND) and
         (previous_distance > INNER_BOUND and previous_distance < OUTER_BOUND)):
        # Play a sound in a separate thread, so that it doesn't interrupt the rest of our code (currently disabled)
        #player.play()
        # Call our message displaying functions to write messages to the screen about what has just happened
        display_detection("Moving out of the detection zone")
        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
        display_measured(measured)

    # If motionless, or outside the monitored range
    # TODO motionless is a separate, interesting state which we should identify and treat separately
    else:
        # sys.stdout.write("\u001b[17;1H")        # start at a consistent position in window
        display_detection("No movement, or out of range")                   # echo response is out of range

    # Keep a historical record (previous_distance) of the latest distance (current_distance) of something detected
    # so that we can compare against it next time something is detected
    previous_distance = current_distance

    # ------------------- end of code --------------------
