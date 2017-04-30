
import time
import Adafruit_MCP4725


"""CONSTANTES"""
DAC_min = 986 #equivale a 1.3V
DAC_0 = 1744 #equivale a 2.3V
DAC_max = 2503 #equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0 #intervalo maximo de variacao positiva 2.3V a 3.3V
max_variacao_neg = DAC_0 - DAC_min #intervalo maximo de variacao negativa 2.3V a 1.3V
#

#  Create a DAC instance.
dac1 = Adafruit_MCP4725.MCP4725(0x62)
dac2 = Adafruit_MCP4725.MCP4725(0x63)

# Note you can change the I2C address from its default (0x62), and/or the I2C
# bus by passing in these optional parameters:
#dac = Adafruit_MCP4725.MCP4725(address=0x49, busnum=1)

# Loop forever alternating through different voltage outputs.
print('Press Ctrl-C to quit...')

while True:
    print('Setting voltage to 1.3V')
    dac1.set_voltage(DAC_min)
    dac2.set_voltage(DAC_min)
    time.sleep(2.0)
    print('Setting voltage to 2.3V!')
    dac1.set_voltage(DAC_0)  # 2048 = half of 4096
    dac2.set_voltage(DAC_0)
    time.sleep(2.0)
    print('Setting voltage to 3.3V!')
    dac1.set_voltage(DAC_max, True)
    dac2.set_voltage(DAC_max, True)
    time.sleep(2.0)