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
siglen=2
filepath = r'D:\\data\\Tao\\B1-20200116-another\\KQtestwANS100Hz-2\\'
name = 'data.txt'


Vbiasdac=1
Vin1dac=2
Vin2dac=3


ivvi = InstrumentImporter.IVVIrack.initInstrument()
Vgain=1
V_low=-0.5/Vgain
V_high=0.5/Vgain
V_step=0.01/Vgain
Input1 = np.linspace(0, V_low, int(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, int((V_high-V_low)/V_step)+1)+V_step/2
Input3 = np.linspace(V_high, 0, int(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
InstrumentImporter.reset(0,0, exit=False)


for vbias in Input:
	for vin1 in np.linspace(-0.25,0.25,26):
		for vin2 in np.linspace(-0.25,0.25,26):
			CV=np.array([vbias,vin1,vin2])
			InstrumentImporter.IVVIrack.setControlVoltages(ivvi, CV[0:2]*1000)
			print(CV)
			time.sleep(0.1)
			x = np.zeros((2,siglen*Fs))
			adwin=InstrumentImporter.adwinIO.initInstrument()
			Output = InstrumentImporter.adwinIO.IO(adwin,x,Fs)*Igain
			datetime = time.strftime("%d_%m_%Y_%H%M%S")
			fp = filepath +'/'+ datetime + '_vbias_' + str(vbias*Vgain) +'_vin1_'+str(vin1)+ '_vin2_'+str(vin2)+'_'+name
			np.savetxt(fp,Output.transpose())


InstrumentImporter.reset(0,0)