# 1FSK-Modulation-Demodulation
The repository contains Python code to show modulation/demodulation procedures for data transmitting via DAC-ADC channel.

## General information
The main purpose of this repository is given information about the basic principles of 1FSK modulation and demodulation. DAC and ADC are used to generate and receive the data signal. These basics may be useful in more serious projects like wireless data transmitting.

Using devices:
1) BeagleBone Black (BBB) platform on Debian 9
2) DAC -- I2C connected MCP4725 (12-bit, High-Speed Mode available). Arduino shield with MCP4725 is used (https://amperka.ru/product/troyka-dac-screw-terminal)
3) ADC -- onboard.

There are two sections with two different demodulation algorithm:
1) Algorithm with spectral math conversions (more appropriate) (https://github.com/dmt0768/1FSK-Modulation-Demodulation/tree/new/Сonversions%20in%20the%20time%20domain)
2) Algorithm with conversions in the time domain (https://github.com/dmt0768/1FSK-Modulation-Demodulation/tree/new/Spectral%20conversions)

Open folders to see the repositories.