import time
import matplotlib.pyplot as plt

from SkyNEt.instruments import InstrumentImporter
import numpy as np
import time

Sourcegain = 1
Igain = 100			#use to make output in nA
Vgain = 5
V_low = -3/Vgain			#needs to be 0 or negative
V_high = 2/Vgain		#needs to be 0 or positive
V_step = 0.05/Vgain   #change stepsize 
Fs = 400 						#change sample frequency
SL = 300 #in seconds
filepath = r'D:\\data\\Tao\\191204-B-Nsub-2min-another-50nm-largerange\\BiasNoisewANS100Hz\\'
name = 'p5 to p4'
instrument = 0  #choose between nidaq (1) and adwin (0)


# Generate the disred input sequence
Input1 = np.linspace(0, V_low, int(abs(V_low/V_step))+1)
Input2 = np.linspace(V_low, V_high, int((V_high-V_low)/V_step)+1)+V_step/2
Input3 = np.linspace(V_high, 0, int(V_high/V_step)+1)

Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
Input[0:len(Input1)] = Input1
Input[len(Input1):len(Input1)+len(Input2)] = Input2
Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
Inputadwin = Input/Sourcegain
print(Inputadwin)

for InputV in Inputadwin:
    x=np.ones(Fs*SL)*InputV
    print('Input voltage:')
    print(InputV)   
    if  instrument == 0:
        adwin=InstrumentImporter.adwinIO.initInstrument()
        output = InstrumentImporter.adwinIO.IO(adwin,x,Fs)[0]
        output = np.array(output) * Igain
    elif instrument == 1:
        output = nidaqIO.IO(x, Fs)
        output = np.array(output) * Igain
    else:
        print('specify measurement device')

    # plt.figure()
    # plt.plot(output)
    # plt.show()

    datetime = time.strftime("%d_%m_%Y_%H%M%S")
    filename = filepath + '\\' + datetime 
    np.savetxt(filename, np.insert(output,0,InputV*Vgain))



