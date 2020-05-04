#!/usr/bin/python3

print('Program is started')

import numpy as np
from scipy.signal.signaltools import medfilt
from scipy.signal.signaltools import hilbert

print('Libs are loaded')

N = 8 + 1  # Amount of bits
Fbit = 10  # bitrate
dur = 1/Fbit * N  # Duration of signal

'''
Data in
'''

y = list()

with open('buffer.txt', 'r') as f:
    for line in f:
        if line != '\n' or '':
            y.append(int(line.strip()))

print('File is loaded')

"""
DETECTOR
"""
print('Diff launch')
y_diff = np.diff(y,1)  # differentiator
print('Hilbert launch')
y_env = np.abs(hilbert(y_diff))  # Hilbert' filter
print('Medfilt launch')
m_w = int(len(y)/30)  # Median filter's window
y_filtered = medfilt(y_env, m_w + (m_w+1) % 2)   # Median filter
print('Norm code')
y_filtered = y_filtered / max(y_filtered)  # Signal normalization
print('Code processing')

code = list()
for i in range(0,N):
    if y_filtered[ int( (1/(2*Fbit) + i/Fbit) / (dur/len(y)) ) ] >= 0.75:
        code.append(1)  # High level
    elif y_filtered[ int( (1/(2*Fbit) + i/Fbit) / (dur/len(y)) ) ] <= 0.55:
        code.append(0)  # low level
    else:
        code.append('?')  # Undetected
print(*code[1:])



