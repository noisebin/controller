from gpiozero import MCP3008
adc = MCP3008(channel=0)
count = 0
values = []
while True:
    adc_in_volts = round(adc.value*3.3,1)#  round down to reduce no. of unique values
    if not adc_in_volts in values:
        values.append(adc_in_volts)
        count+=1
        print(count, "  ,","ADC Value =", round(adc.value, 1),"  ,","Volts in = ", adc_in_volts)