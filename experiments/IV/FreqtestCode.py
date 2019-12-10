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

filepath = r'D:\\data\\Tao\\191204-B-Nsub-2min-another-50nm\\FreqTestwANS100Hz-2\\'

fs = 500
siglen = 10 # seconds
freq = np.logspace(-1,2.3,30)
V_low=0
V_high=1.5
V_step=0.1
Input1 = np.linspace(0, V_low, int(V_low/V_step)+1)
Input2 = np.linspace(V_low, V_high, int((V_high-V_low)/V_step)+1)
Input3 = np.linspace(V_high, 0, int(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3

for vbias in Input:
	for ii in freq:
		print(vbias)
		print(ii)
		x = np.zeros([2,siglen*fs])
		x[0] = 0.01*np.sin(2*np.pi*ii*np.arange(siglen*fs)/fs)+vbias
		adwin=InstrumentImporter.adwinIO.initInstrument()
		output = InstrumentImporter.adwinIO.IO(adwin,x,fs) 
		output = np.array(output)  
		datetime = time.strftime("%d_%m_%Y_%H%M%S")
		fp = filepath + '/' + datetime + '_vbias_'+str(vbias)+'_freq_'+str(ii) + '_Hz'+'.txt'
		np.savetxt(fp,output)
    

InstrumentImporter.reset(0,0)