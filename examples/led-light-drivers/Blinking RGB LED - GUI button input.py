# Program asks for user input to determine color to shine.
# Uses Tk GUI to offer buttons on screen

#  import time, sys
import RPi.GPIO as GPIO
from tkinter import *   #importing the TKinter GUI interface design library
GPIO.setwarnings(False)

redPin = 11   #Set to appropriate GPIO
greenPin = 13 #Should be set in the
bluePin = 15  #GPIO.BOARD format

def blink(pin):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

# print("""Ensure the following GPIO connections: R-11, G-13, B-15
# Colors: Red, Green, Blue, Yellow, Cyan, Magenta, and White
# Use the format: color on/color off""")
#  close window
def close_window():
    window.destroy()
    GPIO.cleanup()

#  create window
window = Tk()
window.title ('RGB LED On or Off')
window.geometry ('250x350')

#  change colours using buttons
def main():
#  create on buttons
    red_button = Button (window, text = 'Red on', width=10, command = redOn)
    red_button.grid(row=0,column=0,)
    green_button = Button (window, text = 'Green on', width=10, command = greenOn)
    green_button.grid(row=1,column=0)
    blue_button = Button (window, text = 'Blue on', width=10, command = blueOn)
    blue_button.grid(row=2,column=0)
    yellow_button = Button (window, text = 'Yellow on', width=10, command = yellowOn)
    yellow_button.grid(row=3,column=0)
    cyan_button = Button (window, text = 'Cyan on', width=10, command = cyanOn)
    cyan_button.grid(row=4,column=0)
    magneta_button = Button (window, text = 'Magenta on', width=10, command = magentaOn)
    magneta_button.grid(row=5,column=0)
    white_button = Button (window, text = 'White on', width=10, command = whiteOn)
    white_button.grid(row=6,column=0)
    red_button = Button (window, text = 'Red off', width=10, command = redOff)
    red_button.grid(row=0,column=1)
    green_button = Button (window, text = 'Green off', width=10, command = greenOff)
    green_button.grid(row=1,column=1)
    blue_button = Button (window, text = 'Blue off', width=10, command = blueOff)
    blue_button.grid(row=2,column=1)
    yellow_button = Button (window, text = 'Yellow off', width=10, command = yellowOff)
    yellow_button.grid(row=3,column=1)
    cyan_button = Button (window, text = 'Cyan off', width=10, command = cyanOff)
    cyan_button.grid(row=4,column=1)
    magneta_button = Button (window, text = 'Magenta off', width=10, command = magentaOff)
    magneta_button.grid(row=5,column=1)
    white_button = Button (window, text = 'White off', width=10, command = whiteOff)
    white_button.grid(row=6,column=1)
    close_button = Button (window, text = 'Close', width=10, command = close_window)
    close_button.grid(row=7,column=0)
    return


main()