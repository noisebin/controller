import argparse
from noisebin import Noisebin
parser = argparse.ArgumentParser()
parser.add_argument("--sensor", '-s')
args = parser.parse_args()
print(args.sensor)
detectbottles = (args.sensor == "l" or args.sensor == "laser")
detectpeople = (args.sensor == "u" or args.sensor == "ultra")



if detectpeople == True:
    print ("hey, there are people here !!")
    noisebin = Noisebin('u')
else:
    print ('Not looking for people')
if detectbottles == True:
    print ('whoops - that was a bottle')
    noisebin = Noisebin('l')
else:
    print ("not looking for bottles") 
