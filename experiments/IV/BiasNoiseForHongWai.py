import time
import matplotlib.pyplot as plt

from SkyNEt.instruments import InstrumentImporter
import numpy as np
import time
ivvi = InstrumentImporter.IVVIrack.initInstrument()
Sourcegain = 1
Igain = 1000			#use to make output in nA
Vgain = 1
V_low = 0/Vgain			#needs to be 0 or negative
V_high = 1/Vgain		#needs to be 0 or positive
V_step = 0.2/Vgain   #change stepsize 
Fs = 500 						#change sample frequency
SL = 30 #in seconds
filepath = r'D:\\data\\Tao\\Hongwai20200703\\TDependent\\1571\\310K\\Gate-6V\\'
name = '1571'
instrument = 0  #choose between nidaq (1) and adwin (0)


# Generate the disred input sequence
# Input1 = np.linspace(0, V_low, round(abs(V_low/V_step))+1)
# Input2 = np.linspace(V_low, V_high, round((V_high-V_low)/V_step)+1)+V_step/2
# Input3 = np.linspace(V_high, 0, round(V_high/V_step)+1)

# Input = np.zeros(len(Input1)+len(Input2)+len(Input3))
# Input[0:len(Input1)] = Input1
# Input[len(Input1):len(Input1)+len(Input2)] = Input2
# Input[len(Input1)+len(Input2):len(Input1)+len(Input2)+len(Input3)] = Input3
InstrumentImporter.IVVIrack.setControlVoltages(ivvi, np.array([-6*1000/5]))
Input = np.linspace(V_low, V_high, round(abs(V_high/V_step))+1)
Inputadwin = Input/Sourcegain
print(Inputadwin)

for InputV in Inputadwin:
    fcount=1

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
    print(np.average(output.transpose())) 
    datetime = time.strftime("%d_%m_%Y_%H%M%S")
    filename = filepath + '\\' + str(fcount) +'_'+ datetime + '_vbias_' + str(InputV) +'.txt'
    np.savetxt(filename, np.insert(output,0,InputV*Vgain))
    fcount=fcount+1

InstrumentImporter.reset(0,0)

