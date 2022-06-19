#  Ref: https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/5
# with wind speed, gust speed and direction
from gpiozero import Button, MCP3008
import time
import math
import statistics  # used to determine wind gusts
adc = MCP3008(channel=0)
#  print(adc.value)
store_speeds = []
wind_speed_sensor = Button(5)
wind_count = 0  # counts how many half-rotations
radius_cm = 8.0  # radius of Davis anemometer
wind_interval = 5  # how often (secs) to report speed. Default = 5

# every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
#    print("spin" + str(wind_count))
CM_IN_A_KM = 100000.0
SECS_IN_A_HOUR = 3600
ADJUSTMENT = 1.32629  # anemometer factor compensation value. default 1.18

# calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 1.0

    # calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / CM_IN_A_KM

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_A_HOUR

    return km_per_hour * ADJUSTMENT

wind_speed_sensor.when_pressed = spin

def reset_wind():
    global wind_count
    wind_count = 0

# wind gust calculations
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = round(calculate_speed(wind_interval), 2)
        store_speeds.append(final_speed)
    wind_gust = round(max(store_speeds), 2)
    wind_speed = round(statistics.mean(store_speeds), 2)
    print(final_speed, wind_gust)