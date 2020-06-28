#!/usr/bin/python3

import time
import Adafruit_BBIO.GPIO as GPIO

ADC_T = 0.001  # How often the program will read data from ADC
GPIO.setup('P8_8', GPIO.IN)  # GPIO line for triggering this program
adc_path = '/sys/bus/iio/devices/iio:device0/in_voltage3_raw' # ADC's file path

time_point = 0  # Used for the time delay (seconds)
f = open(adc_path, 'r')  # Open ADC file
buf = open('buffer.txt', 'w')  # Name of my buffer
print('Wait for edge...')
GPIO.wait_for_edge('P8_8', GPIO.BOTH)  # Trigger for edge on GPIO line
while GPIO.input('P8_8'):  # While the GPIO line is high
    while time.time() - time_point < ADC_T:  # Time delay
        None
    N = int(f.read())  # Read the ADC's file
    buf.write(str(N) + '\n')  # Write to buffer
    time_point = time.time()
    f.seek(0)  # set pointer in ADC's file to the start position

f.close()
buf.close()