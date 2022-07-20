# https://peppe8o.com/download/python/shift_register.py

import RPi.GPIO as GPIO
import sys

#define PINs according to cabling
dataPIN = 16
latchPIN = 20
clockPIN = 21

#set pins to putput
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPIN,latchPIN,clockPIN),GPIO.OUT)

#define shift register update function
def shift_update(input,data,clock,latch):
  #put latch down to start data sending
  GPIO.output(clock,0)
  GPIO.output(latch,0)
  GPIO.output(clock,1)

  #load data in reverse order
  for i in range(7, -1, -1):
    GPIO.output(clock,0)
    GPIO.output(data, int(input[i]))
    GPIO.output(clock,1)

  #put latch up to store data on register
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)

#main program, calling shift register function
#uses "sys.argv" to pass arguments from command line
shift_update(sys.argv[1],dataPIN,clockPIN,latchPIN)

#PINs final cleaning
GPIO.cleanup()
