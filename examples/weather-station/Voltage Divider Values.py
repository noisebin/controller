#  as for Noisebin project setup
# r2 direction pot is conected directly to common. r1 to Vcc
# r2 = Wind vane pot
# r1 = fixed resistor
def voltage_divider(r1, r2, Vin):
    Vout = (r2/(r1+r2))*Vin
# incorrect formula on build site:    Vout = (Vin*r1)/(r1+r2)
    return round(Vout, 3)
print(voltage_divider(2000, 20000, 3.3))