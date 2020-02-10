import time
import matplotlib.pyplot as plt
# from instruments.niDAQ import nidaqIO
# from instruments.ADwin import adwinIO
import numpy as np
import time
import modules.SaveLib as SaveLib
from SkyNEt.instruments import InstrumentImporter
Sourcegain = 1
Igain = 10			#use to make output in nA
Fs = 800 						#change sample frequency
siglen=5
filepath = r'D:\\data\\Tao\\B1-20200128\\KQtestwANS100HzOneInput\\'
name = 'data.txt'


Vbiasdac=1


ivvi = InstrumentImporter.IVVIrack.initInstrument()
Vgain=1
V_low=-1.9/Vgain
V_high=1.9/Vgain
V_step=0.05/Vgain
Input1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)+V_step/2
Input3 = np.linspace(V_high, 0, round(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3


Vg_low=-1
Vg_high=1
Vg_step=0.05
Inputg1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
Inputg2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)
Inputg3 = np.linspace(V_high, 0, round(V_high/V_step)+1)

Inputg = np.zeros(len(Inputg1)+len(Inputg2)+len(Inputg3))
Inputg[0:len(Inputg1)] = Inputg1
Inputg[len(Inputg1):len(Inputg1)+len(Inputg2)] = Inputg2
Inputg[len(Inputg1)+len(Inputg2):len(Inputg1)+len(Inputg2)+len(Inputg3)] = Inputg3

InstrumentImporter.reset(0,0, exit=False)


for vbias in Input:
	print(vbias)
	InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([vbias*1000]))
	for Vg in Inputg:
		print(Vg)
		x = np.zeros((2,siglen*Fs))+Vg
		adwin=InstrumentImporter.adwinIO.initInstrument()
		Output = InstrumentImporter.adwinIO.IO(adwin,x,Fs)*Igain
		datetime = time.strftime("%d_%m_%Y_%H%M%S")
		fp = filepath +'/'+ datetime + '_vbias_' + str(vbias*Vgain) +'_vin1_'+str(Vg)+'_'+name
		np.savetxt(fp,Output.transpose())


InstrumentImporter.reset(0,0)