#!/usr/bin/env python

import sys, pygame, time

# channels here refers to the number of physical channels or playback devices
# let's call these physical channels
mixer = pygame.mixer.init(channels=2)

# whereas here it refers to playback channels (they all get mixed down like in a DAW)
# each one can only play one sound at a time.
# lets call them playback channels

# these channels are identical at the moment
left_channel = pygame.mixer.Channel(0)
right_channel = pygame.mixer.Channel(1)

# now we differentiate them
# each float represents the volume on that physical channel
# left, right etc etc
left_channel.set_volume(0, 1)
right_channel.set_volume(1, 0)

# load the sound from the file into memory
# it supports ogg vorbis and uncompressed wav
# if your wav isnt working make sure its uncompressed
# as wav is a kitchen sink format
# use ffmpeg to transcode
# ffmpeg -i inputfile sound.ogg
sound = pygame.mixer.Sound('sound.ogg')

# playback is asyncrenous and will stop if the program exits before it's over so we have to keep it alive
left_channel.play(sound)
time.sleep(1)
right_channel.play(sound)
time.sleep(1)