import time
import matplotlib.pyplot as plt
from SkyNEt.instruments import InstrumentImporter
import numpy as np
import time
ivvi = InstrumentImporter.IVVIrack.initInstrument()
Sourcegain = 1
Igain = 1000			#use to make output in nA
Vgain = 1
Temp = '300K'
VS_low = 0		#needs to be 0 or negative
VS_high = 1		#needs to be 0 or positive
VS_step = 0.2   #change stepsize
InputVS = np.linspace(VS_low, VS_high, round(abs(VS_high/VS_step))+1)/Sourcegain

VG_low = -2/Vgain         #needs to be 0 or negative
VG_high = 2/Vgain        #needs to be 0 or positive
VG_step = 0.2/Vgain   #change stepsize
InputVG = np.linspace(VG_low, VG_high, round(abs(VG_high/VG_step))+1)  
Fs = 500 						#change sample frequency
SL = 30 #in seconds
filepath = r'D:\\data\\Tao\\Hongwai20200703\\TDependent\\1571\\310K\\Gate-6V\\'
instrument = 0  #choose between nidaq (1) and adwin (0)

print(InputVS)
results=np.array([])
VGi=0
for VG in InputVG:
    InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([VG*1000/5]))
    for VS in InputVS:
        x=np.ones(Fs*SL)*VS
        print('Input voltage:')
        print(VS)   
        if  instrument == 0:
            adwin=InstrumentImporter.adwinIO.initInstrument()
            output = InstrumentImporter.adwinIO.IO(adwin,x,Fs)[0]
            output = np.array(output) * Igain
        elif instrument == 1:
            output = nidaqIO.IO(x, Fs)
            output = np.array(output) * Igain
        else:
            print('specify measurement device')
        
        np.append(results,output,axis=VGi)
    VGi=VGi+1
datetime = time.strftime("%d_%m_%Y_%H%M%S")
filename = filepath + '\\' + Temp +'_'+ datetime + '_IVG.npz'
np.save(filename, Gatevoltage=InputVG, sourcevoltage=InputVS, outputcurrent=results)
InstrumentImporter.reset(0,0)

