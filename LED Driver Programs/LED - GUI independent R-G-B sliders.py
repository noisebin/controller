#  thanks to: https://www.mechatronicslab.net/raspberry-pi-multicolor-rgb-led/
#  import necessary libraries
from gpiozero import PWMLED
from tkinter import *

#  change the RGB LED color
def change_color(self):
    red.value = red_slider.get ()
    green.value = green_slider.get ()
    blue.value = blue_slider. get ()
    print (self)

#  close the window
def close_window ():
    window.destroy ()

#  create a PWMLED object for each color
red = PWMLED (22)
green = PWMLED (17)
blue = PWMLED (27)

#  create window
window = Tk ()
window.title ('RGB Variable LED Controller')
window.geometry ('300x200')

#  create three sliders to control each RGB LED lead
red_slider = Scale (window, from_ = 0, to = 1 , resolution = 0.01,
orient = HORIZONTAL, label = 'Red', troughcolor = 'red', length = 200,
command = change_color)
red_slider.pack ()

green_slider = Scale (window, from_ = 0, to = 1, resolution = 0.01,
orient = HORIZONTAL, label = 'Green', troughcolor = 'green', length = 200,
command = change_color)
green_slider.pack ()

blue_slider = Scale (window, from_ = 0, to = 1, resolution = 0.01,
orient = HORIZONTAL, label = 'Blue', troughcolor = 'blue', length = 200,
command = change_color)
blue_slider.pack ()

#  create close button
close_button = Button (window, text = 'Close', command = close_window)
close_button.pack ()

mainloop ()