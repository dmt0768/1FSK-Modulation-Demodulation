## Spectral conversions
In this section, the program algorithm is described. There is only a reduced code necessary for understanding. You could download full code, see the last section.

All code consists of 3 parts: modulation and sending program, receiving program and demodulation program.

### 1. Modulation and sending
The name of the described file is *modulator.py*

- Lybraries loading:

```
from smbus2 import SMBus
import numpy as np
import time
import Adafruit_BBIO.GPIO as GPI
```

*smbus2* is a library to adjust I2C ports.

*numpy* is needed for processing data.

*time* is used for time management.

*Adafruit_BBIO* allows the program to adjust GPIO lines (**This library was developed especially for BBB**).


- I2C constants:

```
chip_adr = 0x63  # This is the address of your DAC chip on the I2C lines
i2c_folder = '/dev/i2c-2'  # This is the folder of your I2C file
max = 2000  # Do not increase it while BBB's onboard ADC is used! 2000 -- recommended, 2200 -- LIMIT
```

- DAC constants:

```
DAC_T = 0.005  # This is a time delay (in seconds) between times of data sending to DAC
GPIO.setup('P8_7',GPIO.OUT)  # A GPIO line is holded on while data is transmitting  

```

- Data processing constants:

```
Fc = 100  # Carrier frequency
Fbit = 10  # Bitrate of data
Fdev = 50  # Frequency deviation, make higher than bitrate
N = 8 + 1  # How many bits to send.
#  One additional bit (+1) is going first and is used as an example for decoder algorithm as high level ("one")
A = max/4 - 10  # Transmitted signal amplitude. Positive voltage DAC and DAC are used
zero_line = max/2  # See above ("A")
Fs = 2000  # sampling frequency must be much higher than the carrier frequency Fc
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

To understand  the last operations see the numpy docs: https://numpy.org/doc/ 

In the result you will get:
![orig_im](https://github.com/dmt0768/hello-world/blob/master/images/1FSK/2020-05-02_18-53-24.png)

- Signal transmitting

DAC connected via I2C is used. So I use this interface, and this part of the program is very special according to my DAC's I2C protocol.
Thus I will omit one. Although, if you are interested in I2C, there is my repository with a full description of this DAC MCP4725 adjusting: https://github.com/dmt0768/Beaglebone-black_I2C-DAC

Here is general information about I2C, which has helped me **(but it in Russian)**: http://easyelectronics.ru/interface-bus-iic-i2c.html


There is one thing worthy of attention. I hold on my GPIO line while data is transmitting. This is the trigger for the receiver.

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

- Preparing and triggering:

```
time_point = 0  # Used for the time delay (seconds)
f = open(adc_path, 'r')  # Open ADC file
buf = open('buffer.txt', 'w')  # Name of my buffer

GPIO.wait_for_edge('P8_8', GPIO.BOTH)  # Trigger for edge on GPIO line
```

Next, there is nothing special, just reading and writing file each *ADC_T* time

```
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

The name of the described file is *decoder.py*

- Libraries loading and constants:

```
import numpy as np
from scipy import signal
```

```
Fc = 2000  # simulate a carrier frequency of 1kHz 5000
Fbit = 10  # simulated bitrate of data
Fdev = 500  # frequency deviation, make higher than bitrate 1000
N = 9  # how many bits to send
A = 1  # transmitted signal amplitude
NADC = len(y) #ADC number of reading
Fs = (N/Fbit/NADC)**(-1)
A_n = 0.3  # noise peak amplitude
N_prntbits = 8  # number of bits to print in plots
```

- Read buffer:

This is just buffer-file reading. I'll omit this part.

- Detector:

To demodulate  signal I use:

1) cos and sin multiply,

- original spectrum:

![decoder](https://github.com/dmt0768/hello-world/blob/master/images/1FSK/image.png)

- multiplied spectrum:


2) Low-frequency pass filter,

- filtered specrtum:

3) arctan2 function.

- origina signal:

- calculated result:


Here is the code of filters:

```
t = np.arange(0, len(y)*1/Fs, 1 / Fs)


y_cos = y * np.cos(2* np.pi * (Fc-Fdev) * t)
y_sin = y * np.sin(2* np.pi * (Fc-Fdev) * t)


sos = signal.butter(7, np.pi * 2000/Fs, output='sos')
y_cos_lpf = signal.sosfilt(sos, y_cos)
y_sin_lpf = signal.sosfilt(sos, y_sin)


angle = np.arctan2(y_sin_lpf, y_cos_lpf)
angle = np.unwrap(angle)

sig = -np.diff(angle,1)
```

- High and low levels detecting:

The first bit of signal is always "one". It is used an example for decoder algorithm as a high level ("one")

```
def win_average(s, num, winsize=200): # Real window's size is winsize+1, use for code recognition, to find windowed average
    delta = round(winsize / 2)
    sum = 0
    for i in range(num-delta, num+delta):
        sum += s[i]
    return sum/(2*delta)
    
code = list()

high_level = win_average(sig, round(Fs/Fbit/2))*0.7
low_level = win_average(sig, round(Fs/Fbit/2)) * 0.3

for i in range(1, N):
    if win_average(sig, round(Fs/Fbit/2 + i*Fs/Fbit)) > high_level:
        code.append(1)
    elif win_average(sig, round(Fs/Fbit/2 + i*Fs/Fbit)) < low_level:
        code.append(0)
    else:
        code.append('?')

print(code)
```

## Download
For the first of all you should update your pip:

```
  pip3 install --upgrade pip
```

Then install python packages:

```
pip3 install smbus2
pip3 install Adafruit_BBIO
pip3 install numpy
pip3 install scipy
```

Download programs from GitHub:

```
  git clone https://github.com/dmt0768/1FSK-Modulation-Demodulation.git
```
