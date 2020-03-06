import time
import matplotlib.pyplot as plt
# from instruments.niDAQ import nidaqIO
# from instruments.ADwin import adwinIO
import numpy as np
import time
import modules.SaveLib as SaveLib
from SkyNEt.instruments import InstrumentImporter




ivvi = InstrumentImporter.IVVIrack.initInstrument()

InstrumentImporter.reset(0,0, exit=False)

filepath = r'D:\\data\\Tao\\B-Nsub-20200228-A-annealed\\BiasSensewANS100Hz-2\\'

fs = 800
siglen = 500 # seconds
Igain =10
freq = 1
Vgain=1
V_low=-0.75/Vgain
V_high=0.75/Vgain
V_step=0.01/Vgain
Input1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)+V_step/2
Input3 = np.linspace(V_high, 0, round(V_high/V_step)+1)


Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
print(Input)
for vbias in Input:

	print(vbias)
	InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([vbias*1000]))
	x = np.zeros([2,siglen*fs])
	x[0] = 0.1*np.sin(2*np.pi*freq*np.arange(siglen*fs)/fs)
	adwin=InstrumentImporter.adwinIO.initInstrument()
	output = InstrumentImporter.adwinIO.IO(adwin,x,fs) 
	output = np.array(output)*Igain
	print(np.average(output.transpose()))  
	datetime = time.strftime("%d_%m_%Y_%H%M%S")
	fp = filepath + '/' + datetime + '_vbias_'+str(vbias)+'_freq_'+str(freq) + '_Hz'+'.txt'
	np.savetxt(fp,output.transpose())
    

InstrumentImporter.reset(0,0)