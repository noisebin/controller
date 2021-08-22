    #  Ref: https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/5

from gpiozero import Button
import time
import math

wind_speed_sensor = Button(18)
wind_count = 0  # counts how many half-rotations
radius_cm = 8.0  # radius of Davis anemometer
wind_interval = 1  # how often (secs) to report speed. Normally 5

    # every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    #    print("spin" + str(wind_count))
CM_IN_A_KM = 100000.0
SECS_IN_A_HOUR = 3600
ADJUSTMENT  = 1.18 # final value to be determined and updated

    # calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / CM_IN_A_KM

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_A_HOUR

    return km_per_hour * ADJUSTMENT

    # print(speed)
wind_speed_sensor.when_pressed = spin

while True:
    wind_count = 0
    time.sleep(wind_interval)

    print(calculate_speed(wind_interval), "km/h")

def reset_wind():
    global wind_count
    wind_count = 0
    # to measure wind direction an Analogue to Digital converter is needed like a MCP3008


