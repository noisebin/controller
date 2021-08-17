# LED colour selected by keyboard commands, i.e. <colour> [on | off]
# Modified from project: https://www.instructables.com/Using-a-RPi-to-Control-an-RGB-LED/
import sys, time
import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

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

def greenOn():
    blink(greenPin)

def blueOn():
    blink(bluePin)

def yellowOn():
    blink(redPinPin)
    blink(greenPin)

def cyanOn():
    blick(greenPin)
    blink(bluePin)

def magnetaOn():
    blink(redPin)
    blink(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

#  Turn each light off
def redOff():
	turnOff(redPin)

def greenOff():
	turnOff(greenPin)

def blueOff():
	turnOff(bluePin)

def yellowOff():
	turnOff(redPin)
	turnOff(greenPin)

def cyanOff():
	turnOff(greenPin)
	turnOff(bluePin)

def magentaOff():
	turnOff(redPin)
	turnOff(bluePin)

def whiteOff():
	turnOff(redPin)
	turnOff(greenPin)
	turnOff(bluePin)
#  Ask use for colour to turn on or off
def main():
        while True:
            cmd = raw_input("Choose an option:")
            if cmd == "red on":
                redOn()

            elif cmd == "red off":
                redOff()

            elif cmd == "green on":
                greenOn()

            elif cmd == "green off":
                greenOff()

            elif cmd == "blue on":
                blueOn()
		
            elif cmd == "blue off":
                blueOff()

            elif cmd == "yellow on":
                yellowOn()

            elif cmd == "yellow off":
                yellowOff()

            elif cmd == "cyan on":
                cyanOn()

            elif cmd == "cyan off":
                cyanOff()

            elif cmd == "magenta on":
                magentaOn()

            elif cmd == "magenta off":
                magentaOff()

            elif cmd == "white on":
                whiteOn()

            elif cmd == "white off":
                whiteOff()
            else:
                print("Not a valid command")
        return
main()