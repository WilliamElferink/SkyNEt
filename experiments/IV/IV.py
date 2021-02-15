import time
import matplotlib.pyplot as plt

from SkyNEt.instruments import InstrumentImporter
import numpy as np
import time
ivvi = InstrumentImporter.IVVIrack.initInstrument()

Sourcegain = 1
Igain = 1000		#use to make output in nA
Vgain= 1
V_low = -0.1/Vgain	#needs to be 0 or negative
V_high = 0.1/Vgain	#needs to be 0 or positive
V_steps = 1000*(V_high-V_low) 	#change stepsize 
Fs = 1000 						#change sample frequency
filepath = r'D:\\data\\Tao\\Hongwai20200703\\IVRT1587\\'		
name = 'WideBar1571gate-0V.txt'
instrument = 0  #choose between nidaq (1) and adwin (0)
InstrumentImporter.reset(0,0, exit=False)
InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([0*1000/5]))
# Generate the disred input sequence
Input1 = np.linspace(0, V_low, int((V_steps*V_low)/(V_low-V_high)))
Input2 = np.linspace(V_low, V_high, V_steps)
Input3 = np.linspace(V_high, 0, int((V_steps*V_high)/(V_high-V_low)))

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
Inputadwin = Input/Sourcegain

print(Inputadwin)   
if  instrument == 0:
    adwin=InstrumentImporter.adwinIO.initInstrument()
    output = InstrumentImporter.adwinIO.IO(adwin,Inputadwin,Fs)[0]
    output = np.array(output) * Igain
elif instrument == 1:
    output = nidaqIO.IO(Inputadwin, Fs)
    output = np.array(output) * Igain
else:
    print('specify measurement device')

plt.figure()
plt.plot(Input[0:len(output)]*Vgain, output)
plt.show()

datetime = time.strftime("%d_%m_%Y_%H%M%S")
filepath = filepath + '\\' + datetime + '_' + name
np.savetxt(filepath, (Input*Vgain,output))



