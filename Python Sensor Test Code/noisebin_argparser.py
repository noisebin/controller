import argparse
parser = argparse.ArgumentParser()
parser.add_argument("bottles")
parser.add_argument("people")
args = parser.parse_args()
print(args.bottles)
print(args.people)
detectbottles = args.bottles
detectpeople = args.people

if detectpeople == "true":
    print ("hey, there are people here !!")
else:
    print ('Not looking for people')
if detectbottles == "true":
    print ('whoops - that was a bottle')
else:
    print ("not looking for bottles") 