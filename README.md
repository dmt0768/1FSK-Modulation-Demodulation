# 1FSK-Modulation-Demodulation
The repository contains Python code to show modulation/demodulation procedures to data transmitting via DAC-ADC channel.

## General information
The main purpose of this repository is given information about the basic principles of 1FSK modulation and demodulation. DAC and ADC are used to generate and receive the data signal. These basics may be useful in more serious projects like wireless data transmitting.

Using devices:
1) BeagleBone Black controller on Debian 9
2) DAC -- I2C connected MCP4725 (12-bit, High-Speed Mode available). Arduino shield with MCP4725 is used (https://amperka.ru/product/troyka-dac-screw-terminal)
3) ADC -- onboard.

## Detailed overview
In this section, the program algorithm is described. There is only a reduced code necessary for understanding. You could download full code, see the last section.

The all code consist of 3 parts: modulation and sending prog., receiving prog. and demodulation prog.

### 1. Modulation and sending
The name of described file is *modulator.py*

### 2. Receiving

### 3. Demodulation
