# refer to https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/7
from gpiozero import MCP3008
import time
import math
adc = MCP3008(channel=0)
count = 0
values = []
volts = {2.4: 247,
         2.5: 258,
         2.6: 270,
         2.7: 280,
         2.8: 290,
         2.9: 300,
         3.0: 310,
         3.1: 322,
         3.2: 335,
         3.3: 350,
         2.3: 240,
         2.2: 225,
         2.1: 220,
         2.0: 210,
         1.9: 200,
         1.8: 190,
         1.7: 180,
         1.6: 172,
         1.5: 160,
         1.4: 150,
         1.3: 140,
         1.2: 132,
         1.1: 242,
         1.0: 110,
         0.9: 100,
         0.8: 90,
         0.7: 75,
         0.6: 67,
         0.5: 55,
         0.4: 48,
         0.3: 35,
         0.2: 22,
         0.1: 12,
         0.0: 360}

#while True:
#    wind = round(adc.value*3.3, 1)
#    if wind not in volts:
#        values.append(wind)
#        print(('Unknown value: ' + str(wind)) + ' ' + str(volts[wind]))
#    else:
#        print(('Found: ' + str(wind)) + ' ' + str(volts[wind]))
#  seems to be working to this point

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(length=5):
    data = []
    print("Measuring wind direction for %d seconds..." % length)
    start_time = time.time()

    while time.time() - start_time <= length:
        wind = round(adc.value*3.3, 1)
        if wind not in volts:#  keep only good measurements
            print('Unknown value ' + str(wind))
        else:
            data.append(volts[wind])

    return get_average(data)