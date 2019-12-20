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

filepath = r'D:\\data\\Tao\\191204-B-Nsub-2min-another-50nm\\NDRTestwANS100Hz\\'

fs = 100
siglen = 10 # seconds
freq = 67
V_low=-2
V_high=1.5
V_step=0.05
Input1 = np.linspace(0, V_low, int(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, int((V_high-V_low)/V_step)+1)
Input3 = np.linspace(V_high, 0, int(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3

Vg_low=-0.5
Vg_high=0.5
Vg_step=0.001
Inputg1 = np.linspace(0, Vg_low, int(abs(Vg_low/Vg_step))+1)
Inputg2 = np.linspace(Vg_low, Vg_high, int((Vg_high-Vg_low)/Vg_step)+1)
Inputg3 = np.linspace(Vg_high, 0, int(Vg_high/Vg_step)+1)

Inputg = np.zeros(len(Inputg1)+len(Inputg2)+len(Inputg3))
Inputg[0:len(Inputg1)] = Inputg1
Inputg[len(Inputg1):len(Inputg1)+len(Inputg2)] = Inputg2
Inputg[len(Inputg1)+len(Inputg2):len(Inputg1)+len(Inputg2)+len(Inputg3)] = Inputg3

for vbias in Input:

	print(vbias)
	InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([vbias*1000]))
	x = np.zeros([2,len(Inputg)])
	x[0] = Inputg
	adwin=InstrumentImporter.adwinIO.initInstrument()
	output = InstrumentImporter.adwinIO.IO(adwin,x,fs) 
	output = np.array(output)  
	datetime = time.strftime("%d_%m_%Y_%H%M%S")
	fp = filepath + '/' + datetime + '_vbias_'+str(vbias)+'.txt'
	np.savetxt(fp,(Inputg,output[0]))
    

InstrumentImporter.reset(0,0)