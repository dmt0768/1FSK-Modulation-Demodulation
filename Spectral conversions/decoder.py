
#!/usr/bin/python3

print('libs loading')

import numpy as np
from scipy import signal

def win_average(s, num, winsize=200): # Real window's size is winsize+1, use for code recognition, to find average
    delta = round(winsize / 2)
    sum = 0
    for i in range(num-delta, num+delta):
        sum += s[i]
    return sum/(2*delta)

print('File reading')

y = list()
with open('buffer.txt', 'r') as f:
    for line in f.readlines():
        y.append(int(line.strip()))

y = np.array(y) - np.mean(y)

print('Variable initialization')

Fc = 2000  # simulate a carrier frequency of 1kHz 5000
Fbit = 10  # simulated bitrate of data
Fdev = 500  # frequency deviation, make higher than bitrate 1000
N = 9  # how many bits to send
A = 1  # transmitted signal amplitude
NADC = len(y) #ADC number of reading
Fs = (N/Fbit/NADC)**(-1)
A_n = 0.3  # noise peak amplitude
N_prntbits = 8  # number of bits to print in plots

t = np.arange(0, len(y)*1/Fs, 1 / Fs)

print('cos and sin')

y_cos = y * np.cos(2* np.pi * (Fc-Fdev) * t)
y_sin = y * np.sin(2* np.pi * (Fc-Fdev) * t)

print('filtering')

sos = signal.butter(7, np.pi * 2000/Fs, output='sos')
y_cos_lpf = signal.sosfilt(sos, y_cos)
y_sin_lpf = signal.sosfilt(sos, y_sin)

print('angle')

angle = np.arctan2(y_sin_lpf, y_cos_lpf)
angle = np.unwrap(angle)

sig = -np.diff(angle,1)

print('Code recognition')

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
