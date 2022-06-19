#!/usr/bin/env python3

#  Ref: http://www.d3noob.org/2018/04/this-post-is-part-of-book-raspberry-pi.html

#  !/usr/bin/python
#  encoding:utf-8

# The import command makes separate packages of code available to use in your program
#
import sys # sys gives us access to helpful Operating System commands
import RPi.GPIO as GPIO # GPIO lets us observe or set the Pi's input and output pin electrical voltages
import time  # time lets us make the code 'sleep' for an amount of time
import logging
import curses
# The gpiozero module represents _devices_ by adding useful features on top of the RPi.GPIO module's capabilities.
from gpiozero import LineSensor 
# The LineSensor functions are used here to observe the laser container detection sensor

# from signal import pause
# Pause function causes the Pi to sleep, only continuing when woken by pre-defined events.  Not used?

from multi import Player # Player is the package that has the code to play sounds

import sys, signal
class Noisebin:
    def __init__(self, sensor):
        # create logger named 'nb'
        logger = logging.getLogger('nb')
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler('nb.log')
        fh.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(name)s.%(levelname)s %(message)s')
        fh.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)

        # Prepare the Pi's pins for use
        GPIO.setwarnings(False) # Ignore warnings
        GPIO.cleanup() # Reset the state of the pins
        GPIO.setmode(GPIO.BCM) #  Set GPIO pin numbering

        player = Player('samples/') # Set up the sound player and point it towards the sounds

        if sensor == 'u':
            TRIG = 18 # TRIG is a variable that here holds 18.
                    # We use it to point towards pin 18 on the Pi.
                    # (We want pin 18 to be where we connect the device that
                    # *triggers* an ultrasound pulse).

            ECHO = 24 # ECHO is a variable that here holds 24.
                    # We use it to point towards pin 24 on the Pi.
                    # (We want pin 24 to be where we receive an *echo* from the
                    # ultrasound pulse).

            scaling = 17150 #  Distance / echo time conversion and scaling factor


            GPIO.setup(TRIG, GPIO.OUT)                       #  Define ultrasonic sensor trigger pin as GPIO out
            GPIO.setup(ECHO, GPIO.IN)                        #  Define ultrasonic sensor response pin as GPIO in

            # Declare some variables for the distance measured to an object
            # last distance measurement by the sensor (last_distance) and 
            # the distance measured by the sensor *this time* (current_distance)
            # We set the values of these to be outside our detection zone before beginning,
            # so it will be obvious when an object / person approaches
            current_distance = -1.0
            previous_distance = -1.0

            # Set some variables to hold the values of the boundaries of the 'detection zone'.
            # INNER_BOUND is the inner edge of the detection zone (edge closest to the sensor)
            # OUTER_BOUND is the outer edge of the detection zone (edge furthest away from the sensor)
            # Values are in cm
            INNER_BOUND = 20
            OUTER_BOUND = 200  # 2 metres maximum.  any further away and we're not interested!

            try:
                # Clear and decorate the screen
                self.display_begin()

                # The loop here will continue forever (i.e. while True is True)
                # The indented code is performed within the loop
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

                    # If the measured distances indicate the object is moving into the 'detection zone'
                    if((current_distance > INNER_BOUND and current_distance < OUTER_BOUND) and
                    (previous_distance <= INNER_BOUND or previous_distance >= OUTER_BOUND)):

                        # Play a sound in a separate thread, so that it doesn't interrupt the rest of our code
                        logger.info("Object entered detection zone. About to play a sound.")
                        player.play()

                        # Display messages on the screen about what has just happened
                        self.display_detection("Moving into the detection zone")

                        # f formats a message comprised of multiple parts 
                        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
                        self.display_measured(measured)

                    # If the measured distances indicate the object is moving out of the 'detection zone'
                    elif((current_distance <= INNER_BOUND or current_distance >= OUTER_BOUND) and
                        (previous_distance > INNER_BOUND and previous_distance < OUTER_BOUND)):

                        # Play a sound in a separate thread, so that it doesn't interrupt the rest of our code (currently disabled)
                        #player.play()
                        # Call our message displaying functions to write messages to the screen about what has just happened
                        self.display_detection("Moving out of the detection zone")
                        measured = f'Previous distance: {previous_distance}  Current distance: {current_distance}'
                        self.display_measured(measured)

                    # If motionless, or outside the monitored range
                    # TODO motionless is a separate, interesting state which we should identify and treat separately
                    else:
                        # sys.stdout.write("\u001b[17;1H")        # start at a consistent position in window
                        self.display_detection("No movement, or out of range")                   # echo response is out of range

                    # Keep a historical record (previous_distance) of the latest distance (current_distance) of something detected
                    # so that we can compare against it next time something is detected
                    previous_distance = current_distance

            finally:                # receives control from any exit() statement or program abort (^C)
                print('\nScript exit.\n')
            # ------------------- end of code --------------------

        if sensor == 'l':
            def handle_line():
                logger.info('Waiting for container')

            def handle_no_line(player):
                logger.info('Container detected. Getting ready to play a sound.')
                player.play()

            ContSensor = LineSensor(21) #  Make the Light sensor look for a signal on pin 21
            # Tell the light sensor code to print a message when the line of light is un-broken
            ContSensor.when_line = lambda: handle_line()
            # Tell the light sensor to play a sound when the line of light is broken
            ContSensor.when_no_line = lambda: handle_no_line(player)

            while(True):
                time.sleep(0.1)

    def signal_handler(self, signal, frame):
        print('Signal received.  Hold on a sec.')
        curses.napms(3800)
        sys.exit(0)         # hands over to the finally: clause

    signal.signal(signal.SIGINT, signal_handler)





    # Our program displays information in pre-defined-and-positioned blocks on the screen,
    # to make measurements and events easier to see.
    # The display_begin() function clears the computer screen and prints a title
    # The obscure text codes are called ANSI escape codes, which determine the colour and position of the text which follows.
    # e.g. https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

    def display_begin(self):
        sys.stdout.write("\u001b[1;1H")                  #  start at a consistent position in window
        sys.stdout.write("\u001b[0J")                    #  clear from cursor to bottom of screen
        sys.stdout.write("\u001b[38;5;121m")             #  ESC[38;5;⟨n⟩m Select foreground color
        sys.stdout.write("\u001b[45m")                   #  ESC[45m Select background color

        print("====== NoiseBin Mark 1 (Humanoid Detector) =======")
        sys.stdout.write("\u001b[0m")                    # ESC[39;m reset to default fore/background colors

        print()
        print("Distance measurement in progress")

    # display_detection() displays information from the ultrasonic sensor
    #
    def display_detection(self, status):
        sys.stdout.write("\u001b[13;1H")
        sys.stdout.write("\u001b[0K")                #  Clear to end of line
        print("Status: ", status)

    # display_measured() displays messages about the distance to an object / person from the NoiseBin
    # It uses the ultrasonic sensor and has a range of about 10 metres and precision of ~ 2cm
    #
    def display_measured(self, measured):
        sys.stdout.write("\u001b[15;1H")
        sys.stdout.write("\u001b[0K")                #  Clear to end of line
        print(measured)
        # sys.stdout.write("Status: ")                 #  -

