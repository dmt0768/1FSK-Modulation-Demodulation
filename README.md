# 1FSK-Modulation-Demodulation
The repository contains Python code to show modulation/demodulation procedures to data transmitting via DAC-ADC channel.

## General information
The main purpose of this repository is given information about the basic principles of 1FSK modulation and demodulation. DAC and ADC are used to generate and receive the data signal. These basics may be useful in more serious projects like wireless data transmitting.

Using devices:
1) BeagleBone Black (BBB) platform on Debian 9
2) DAC -- I2C connected MCP4725 (12-bit, High-Speed Mode available). Arduino shield with MCP4725 is used (https://amperka.ru/product/troyka-dac-screw-terminal)
3) ADC -- onboard.

## Detailed overview
In this section, the program algorithm is described. There is only a reduced code necessary for understanding. You could download full code, see the last section.

The all code consist of 3 parts: modulation and sending prog., receiving prog. and demodulation prog.

### 1. Modulation and sending
The name of described file is *modulator.py*

- Lybraries loading:

```
from smbus2 import SMBus
import numpy as np
import time
import Adafruit_BBIO.GPIO as GPI
```

*smbus2* is a lybrary to adjust I2C ports.

*numpy* is needed to processing data.

*time* is used for time management.

*Adafruit_BBIO* allow program to adjust GPIO lines (**This library was developed espesially for BBB**).


- I2C constants:

```
chip_adr = 0x63  # This is adress of your DAC chip on the I2C lines
i2c_folder = '/dev/i2c-2'  # This is forlder of your I2C file
max = 2000  # Do not increase it while BBB's onboard ADC is used! 2000 -- recomended, 2200 -- LIMIT
```

- DAC constants:

```
DAC_T = 0.002  # This is time delay (in seconds) beetwen times of data sending to DAC
GPIO.setup('P8_7',GPIO.OUT)  # This is a GPIO line holding on while data is transmitting  

```

- Data processing constants:

```
Fc = 100  # Carrier frequency
Fbit = 10  # Bitrate of data
Fdev = 50  # Frequency deviation, make higher than bitrate
N = 8 + 1  # How many bits to send.
#  One additional bit (+1) is going first and is used as example for decoder algorithm as high level ("one")
A = max/4 - 10  # Transmitted signal amplitude. Positive voltage DAC and DAC are used
zero_line = max/2  # See above ("A")
Fs = 2000  # sampling frequency, must be much more higher than the carrier frequency Fc
```
- Manual data input in the variable *data_in*

- Data processing:

```
t = np.arange(0, N / Fbit, 1 / Fs)  # time to send all bits
m = np.zeros(0)
for bit in data_in:
    if bit == 0:
        m = np.hstack((m, np.multiply(np.ones(int(Fs / Fbit)), Fc - Fdev)))
    else:
        m = np.hstack((m, np.multiply(np.ones(int(Fs / Fbit)), Fc + Fdev)))

y = np.zeros(0)
y = A * np.cos(2 * np.pi * np.multiply(m, t)) + zero_line
```

To undestand the last operations see the numpy docs: https://numpy.org/doc/ 

In the result you will get:
![orig_im](https://github.com/dmt0768/hello-world/blob/master/images/1FSK/2020-05-02_18-53-24.png)

- Signal transmitting

DAC connected via I2C is used. So I use this interface, and this part of program is very special according to my DAC's I2C protocol.
Thus I will omit one. Althought, if you are interested in I2C, there is my pepository with full description of this DAC MCP4725 adjusting: https://github.com/dmt0768/Beaglebone-black_I2C-DAC

Here is a general infomation about I2C, with has helped me **(but it in Russian)**: http://easyelectronics.ru/interface-bus-iic-i2c.html


There is one thing worthy of attention. I hold on my GPIO line while data is transmitting. This is the trigger for receiver.

```
GPIO.output('P8_7',GPIO.HIGH)  # Trigger line high
    ...
GPIO.output('P8_7', GPIO.LOW)  # Trigger line low
```

### 2. Receiving
The name of described file is *receiver.py*

- Lybraries loading and constants:

```
import time
import Adafruit_BBIO.GPIO as GPIO
```
(see above)


```
ADC_T = 0.001  # How often the program will read data from ADC
GPIO.setup('P8_8', GPIO.IN)  # GPIO line for triggering this program
adc_path = '/sys/bus/iio/devices/iio:device0/in_voltage3_raw' # ADC's file path
```

- Receiving:

There is nothing special, just reading and writing file each *ADC_T* time

```
time_point = 0  # Used for time delay (seconds)
f = open(adc_path, 'r')  # Open ADC file
buf = open('buffer.txt', 'w')  # Name of my buffer
print('Wait for edge...')

GPIO.wait_for_edge('P8_8', GPIO.BOTH)  # Trigger

while GPIO.input('P8_8'):  # While the GPIO line is high

    while time.time() - time_point < ADC_T:  # Time delay
        None
        
    N = int(f.read())  # Read the ADC's file
    buf.write(str(N) + '\n')  # Write to buffer
    time_point = time.time()
    f.seek(0)  # set pointer in ADC's file to the start position

f.close()
buf.close()
```

### 3. Demodulation
