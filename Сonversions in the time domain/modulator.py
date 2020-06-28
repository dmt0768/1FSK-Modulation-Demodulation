#!/usr/bin/python3

from smbus2 import SMBus
import numpy as np
import time
import Adafruit_BBIO.GPIO as GPIO


def send(n):
    if n >= max:
        print('Value error!')
        return
    f_b = n >> 8  # prepearing for DAC I2C protocol
    s_b = n & 0x0ff
    port.write_byte_data(chip_adr, f_b, s_b)


'''
DAC tuning
'''
chip_adr = 0x63  # This is the address of your DAC chip on the I2C lines
i2c_folder = '/dev/i2c-2'  # This is the folder of your I2C file
max = 2000  # Do not increase it while BBB's onboard ADC is used! 2000 -- recommended, 2200 -- LIMIT

DAC_T = 0.005  # This is a time delay (in seconds) between times of data sending to DAC
GPIO.setup('P8_7',GPIO.OUT)  # A GPIO line is holded on while data is transmitting

'''
Signal tuning
'''

Fc = 100  # Carrier frequency
Fbit = 10  # Bitrate of data
Fdev = 50  # Frequency deviation, make higher than bitrate
N = 8 + 1  # How many bits to send.
#  One additional bit (+1) is going first and is used as an example for decoder algorithm as high level ("one")
A = max/4 - 10  # Transmitted signal amplitude. Positive voltage DAC and DAC are used
zero_line = max/2  # See above ("A")
Fs = 2000  # sampling frequency must be much higher than the carrier frequency Fc

data_in = [int(i) for i in input('Enter 8 bits: 0 or 1: ').split()]  # Entering of data
if len(data_in) != (N-1): raise ValueError("Data_in must have 8 numbers!")  # Checking
data_in.insert(0, 1)  # inserting additional "one" (see variable N)

'''
Signal processing
'''

t = np.arange(0, N / Fbit, 1 / Fs)  # time to send all bits
m = np.zeros(0)
for bit in data_in:
    if bit == 0:
        m = np.hstack((m, np.multiply(np.ones(int(Fs / Fbit)), Fc - Fdev)))
    else:
        m = np.hstack((m, np.multiply(np.ones(int(Fs / Fbit)), Fc + Fdev)))

y = np.zeros(0)
y = A * np.cos(2 * np.pi * np.multiply(m, t)) + zero_line

'''
Signal sending
'''

port = SMBus(bus=i2c_folder)
port.open(i2c_folder)
time_point = 0
input('Press Enter to start')
GPIO.output('P8_7',GPIO.HIGH)  # Trigger line high
for i in y:
    i = int(i)
    while time.time() - time_point < DAC_T:  # Time management control
        None
    send(i)
    time_point = time.time()
GPIO.output('P8_7', GPIO.LOW)  # Trigger line low
port.close()

