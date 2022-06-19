    #  Ref: https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/5

from gpiozero import Button
import time
import math

wind_speed_sensor = Button("GPIO5")  # was (18)

wind_count =    0     # counts how many half-rotations
radius_cm =     8.0   # radius of Davis anemometer
wind_interval = 5     # how often (secs) to report speed. Longer sample period averages out variations

#--- Every half-rotation, add 1 to count of rotations (spindle has two microswitches)
def spin():
    global wind_count
    wind_count = wind_count + 1
    # print("spin" + str(wind_count))

CM_IN_A_KM     = 100000.0
CM_IN_A_M      = 100.0
SECS_IN_A_HOUR = 3600
ADJUSTMENT-M-S = 4.55   # total fudge factor.
# final value to be determined and updated
# - different for each device due to manufacturing, age and wear

#--- Calculate the wind speed from the spin count
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    # calculate distance travelled by a cup in cm
    dist_km = circumference_cm * rotations / CM_IN_A_KM
    dist_m = circumference_cm * rotations / CM_IN_A_M

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_A_HOUR
    m_per_sec = dist_m / time_sec

    # return km_per_hour * ADJUSTMENT
    return m_per_sec * ADJUSTMENT

# register call-back for GPIO pulses
wind_speed_sensor.when_pressed = spin

while True:
    wind_count = 0
    time.sleep(wind_interval)

    print(calculate_speed(wind_interval), " m/s")

def reset_wind():
    global wind_count
    wind_count = 0

# To measure wind direction an Analogue to Digital converter is needed like a MCP3008
# - anemometer produces output from a resistive voltage divider


