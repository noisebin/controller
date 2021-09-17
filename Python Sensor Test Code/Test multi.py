#!/usr/bin/env python3

# The import command makes separate packages of code available to use in your program
# Here we are importing some packages that give us the ability to do extra things
import time  # time lets us make the code 'sleep' for an amount of time
from multi import Player # Player is the package that has the code to play sounds

player = Player('samples/') # Set up the sound player and point it towards the sounds

# Play a sound in a separate thread, so that it doesn't interrupt the rest of our code
player.play()
time.sleep(0.1)
player.play()
time.sleep(0.5)
player.play()
time.sleep(1)
player.play()
time.sleep(5)
# ------------------- end of code --------------------
