from gpiozero import RGBLED
from time import sleep
from __future__ import division  # required for python 2

led = RGBLED(red=9, green=10, blue=11)

led.red = 1  # full red
sleep(1)
led.red = 0.5  # half red
sleep(1)

led.color = (0, 1, 0)  # full green
sleep(1)
led.color = (1, 0, 1)  # magenta
sleep(1)
led.color = (1, 1, 0)  # yellow
sleep(1)
led.color = (0, 1, 1)  # cyan
sleep(1)
led.color = (1, 1, 1)  # white
sleep(1)

led.color = (0, 0, 0)  # off
sleep(1)

# slowly increase intensity of blue
for n in range(100):
    led.blue = n/100
    sleep(0.1)


# from gpiozero import RGBLED import psutil, time
# from gpiozero import RGBLED from time import sleep
# led = RGBLED(14, 15, 18)
# led.red = 1  # full red sleep(1)
# led.red = 0.5  # half red sleep(1)
# led.color = (0, 1, 0)  # full green sleep(1)
# led.color = (1, 0, 1)  # magenta sleep(1)
# led.color = (1, 1, 0)  # yellow sleep(1)
# led.color = (0, 1, 1)  # cyan sleep(1)
# led.color = (1, 1, 1)  # white sleep(1)
# led.color = (0, 0, 0)  # off sleep(1)
# # slowly increase intensity of blue
# for n in range(100):
#     led.blue = n / 100 sleep(0.1)
#     ch5listing2.py
# myled = RGBLED(14, 15, 18)
# while True:
# cpu = psutil.cpu_percent() r = cpu / 100.0
# g = (100 - cpu) / 100.0 b = 0
# myled.color = (r, g, b) time.sleep(0.1)
