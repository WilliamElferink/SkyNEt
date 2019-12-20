import modules.ReservoirFull as Reservoir
import modules.PlotBuilder as PlotBuilder
import modules.GenerateInput as GenerateInput
import modules.Evolution as Evolution
import modules.PostProcess as PostProcess
import modules.SaveLib as SaveLib
from instruments.ADwin import adwinIO
from instruments.DAC import IVVIrack
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import time
# temporary imports
import numpy as np



# Read config.txt file
exec(open("config.txt").read())


# initialize benchmark
# Obtain benchmark input
[t, inp] = GenerateInput.softwareInput(
    benchmark, SampleFreq, WavePeriods, WaveFrequency)
adw = adwinIO.initInstrument()


output = adwinIO.IO(adw, inp, SampleFreq)
datetime = time.strftime("%Y_%m_%d_%H%M%S")
np.savetxt('D:/data/Bram/Waves/'+datetime+'.txt', (output, inp, t))

plt.figure(1)
plt.plot(t, output)
plt.plot(t, inp)
plt.suptitle('1_5Hz device output', fontsize=16)
plt.xlabel('time (s)', fontsize=16)
plt.ylabel('current (nA)', fontsize=16)


plt.figure(2)
y = fft.fft(output)
x = np.linspace(0.0, 1.0/(2.0*(1/1000)), len(output)/2)
plt.plot(x, 2.0/len(output) * np.abs(y[:len(output)//2]))
plt.suptitle('1_5 Hz fft', fontsize=16)
plt.xlabel('frequency (Hz)', fontsize=16)
plt.ylabel('intensity', fontsize=16)

adwinIO.IO(adw, np.array([0]), SampleFreq)

# plt.figure(3)
# y = fft.fft(inp)
# x = np.linspace(0.0, 1.0/(2.0*(1/1000)), len(inp)/2)
# plt.plot(x, 2.0/len(inp) * np.abs(y[:len(inp)//2]))
# plt.suptitle('8.5 Hz fft input', fontsize=16)
# plt.xlabel('frequency (Hz)', fontsize=16)
# plt.ylabel('intensity', fontsize=16)


# plt.show()

plt.show()
