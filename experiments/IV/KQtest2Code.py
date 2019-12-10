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
Fs = 2000 						#change sample frequency
siglen=10000
filepath = r'D:\\data\\Tao\\Xdevice\\KQtest2\\'
name = 'data.txt'


Vbiasdac=1
Vin1dac=2
Vin2dac=3


ivvi = InstrumentImporter.IVVIrack.initInstrument()


InstrumentImporter.reset(0,0, exit=False)


for vbias in np.linspace(0,0.5,26):
	for vin1 in np.linspace(-0.2,0.2,11):
		for vin2 in np.linspace(-0.2,0.2,11):
			CV=np.array([vbias,vin1,vin2])
			InstrumentImporter.IVVIrack.setControlVoltages(ivvi, CV[0:2])
			print(CV)
			time.sleep(0.5)
			x = np.zeros((2,siglen))
			Output = InstrumentImporter.nidaqIO.IO(x, Fs)*Igain
			datetime = time.strftime("%d_%m_%Y_%H%M%S")
			fp = filepath +'/'+ datetime + '_vbias_' + str(vbias) +'_vin1_'+str(vin1)+ '_vin2_'+str(vin2)+'_'+name
			np.savetxt(fp,Output)

for vbias in np.linspace(0.25,0.45,21):
	for vin1 in np.linspace(-0.2,0.2,11):
		for vin2 in np.linspace(-0.2,0.2,11):
			CV=np.array([vbias,vin1,vin2])
			InstrumentImporter.IVVIrack.setControlVoltages(ivvi, CV[0:2])
			print(CV)
			time.sleep(0.5)
			x = np.zeros((2,siglen))
			Output = InstrumentImporter.nidaqIO.IO(x, Fs)*Igain
			datetime = time.strftime("%d_%m_%Y_%H%M%S")
			fp = filepath +'/'+ datetime + '_vbias_' + str(vbias) +'_vin1_'+str(vin1)+ '_vin2_'+str(vin2)+'_'+name
			np.savetxt(fp,Output)

InstrumentImporter.reset(0,0)