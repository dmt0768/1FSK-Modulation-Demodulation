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
Fs = 2000  # sampling frequency, must be much more higher than the carrier frequency
```

### 2. Receiving

### 3. Demodulation
