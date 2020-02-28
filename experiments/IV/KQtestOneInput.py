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
freq = 1
siglen=10
filepath = r'D:\\data\\Tao\\A1-20200128-aaanother\\KQtestwANS100HzOneInput-lockin\\'
name = 'p8 p7 p4.txt'


Vbiasdac=1


ivvi = InstrumentImporter.IVVIrack.initInstrument()
Vgain=1
V_low=-1.5/Vgain
V_high=1.4/Vgain
V_step=0.02/Vgain
Input1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)+V_step/2
Input3 = np.linspace(V_high, 0, round(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3


Vg_low=-0.6
Vg_high=0.6
Vg_step=0.03
Inputg1 = np.linspace(0, Vg_low, round(abs(Vg_low/Vg_step))+1)
Inputg2 = np.linspace(Vg_low, Vg_high, round((Vg_high-Vg_low)/Vg_step)+1)
Inputg3 = np.linspace(Vg_high, 0, round(Vg_high/Vg_step)+1)

Inputg = np.zeros(len(Inputg1)+len(Inputg2)+len(Inputg3))
Inputg[0:len(Inputg1)] = Inputg1
Inputg[len(Inputg1):len(Inputg1)+len(Inputg2)] = Inputg2
Inputg[len(Inputg1)+len(Inputg2):len(Inputg1)+len(Inputg2)+len(Inputg3)] = Inputg3

InstrumentImporter.reset(0,0, exit=False)


for vbias in Input:
	print(vbias)
	InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([vbias*1000]))
	for Vg in Inputg:
		print('Vg:')
		print(Vg)
		x = Vg
		adwin=InstrumentImporter.adwinIO.initInstrument()
		Output = InstrumentImporter.adwinIO.IO(adwin,x,Fs)*Igain
		datetime = time.strftime("%d_%m_%Y_%H%M%S")
		fp = filepath +'/'+ datetime + '_vbias_' + str(vbias*Vgain) +'_vin1_'+str(Vg)+'_'+name
		np.savetxt(fp,Output.transpose())


InstrumentImporter.reset(0,0)