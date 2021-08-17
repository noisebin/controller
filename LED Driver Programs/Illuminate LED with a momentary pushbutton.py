# switching on LED using a Toggle Switch but only turning on when the switch is held on

from gpiozero import Button, LED
from signal import pause
button = Button(2)
led = LED(17)

button_when_pressed = led.on
button_when_released = led.off

pause()