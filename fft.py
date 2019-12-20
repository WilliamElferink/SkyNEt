import numpy as np 
import matplotlib.pyplot as plt
import scipy.fftpack as fft

data = np.loadtxt('C:/Users/VenB/Desktop/python/data/AgAgs/Dev22_posE2_freq30Hz.txt') 

plt.rcParams.update({'font.size': 14})

plt.figure(1)
plt.plot(data[0],data[1])
plt.plot(data[0],data[2])
plt.suptitle('8.5Hz device output', fontsize=16)
plt.xlabel('time (s)', fontsize=16)
plt.ylabel('current (nA)', fontsize=16)


plt.figure(2)
y = fft.fft(data[1])
x = np.linspace(0.0, 1.0/(2.0*(1/1000)), len(data[1])/2)
plt.plot(x, 2.0/len(data[1]) * np.abs(y[:len(data[1])//2]))
plt.suptitle('8.5 Hz fft', fontsize=16)
plt.xlabel('frequency (Hz)', fontsize=16)
plt.ylabel('intensity', fontsize=16)

plt.figure(3)
y = fft.fft(data[2])
x = np.linspace(0.0, 1.0/(2.0*(1/1000)), len(data[2])/2)
plt.plot(x, 2.0/len(data[2]) * np.abs(y[:len(data[2])//2]))
plt.suptitle('8.5 Hz fft input', fontsize=16)
plt.xlabel('frequency (Hz)', fontsize=16)
plt.ylabel('intensity', fontsize=16)


plt.show()
