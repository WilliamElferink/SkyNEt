import time
import matplotlib.pyplot as plt
# from instruments.niDAQ import nidaqIO
# from instruments.ADwin import adwinIO
import numpy as np
import time
import modules.SaveLib as SaveLib
from SkyNEt.instruments import InstrumentImporter



# ivvi = InstrumentImporter.IVVIrack.initInstrument()


InstrumentImporter.reset(0,0, exit=False)

filepath = r'D:\\data\\Tao\\Hongwai20200624\\FreqtestwANS100Hz\\'

fs = 800
siglen = 10 # seconds
freq = np.logspace(-1,2.6,50)
V_low=0
V_high=0.1
V_step=0.05
Igain=1000
# Input1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
# Input2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)+V_step/2
# Input3 = np.linspace(V_high, 0, round(V_high/V_step)+1)

# Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
# Input[0:len(Input1)] = Input1
# Input[len(Input1):len(Input1)+len(Input2)] = Input2
# Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
Input = np.linspace(V_low, V_high, round(abs(V_high/V_step))+1)
print(Input)
for vbias in Input:
	for ii in freq:
		print(vbias)
		print(ii)
		x = np.zeros([2,siglen*fs])
		x[0] = 0.01*np.sin(2*np.pi*ii*np.arange(siglen*fs)/fs)+vbias
		adwin=InstrumentImporter.adwinIO.initInstrument()
		output = InstrumentImporter.adwinIO.IO(adwin,x,fs) 
		output = np.array(output)*Igain  
		datetime = time.strftime("%d_%m_%Y_%H%M%S")
		fp = filepath + '/' + datetime + '_vbias_'+str(vbias)+'_freq_'+str(ii) + '_Hz'+'.txt'
		np.savetxt(fp,output)
    

InstrumentImporter.reset(0,0)