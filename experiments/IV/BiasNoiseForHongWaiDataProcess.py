"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import os
from scipy import signal
import matplotlib.pyplot as plt
import timeit


path = r"C:/Users/ChenT/Desktop/Results/TCTO_B_HBPS_oxideremoved/T/"
directories = os.listdir(path+'/Data')
pppath = path+'/Processed/'
if not os.path.exists(pppath):
    os.makedirs(pppath)

fftlen=1024*10
fftoverlap=1024*9

for file in directories:
    print(file)
    t=float(file.split('_')[0][0:-1])
    data=np.load(path+'/Data/'+file)
    gatevoltage=data['Gatevoltage']
    sourcevoltage=data['Sourcevoltage']
    outputcurrent=data['Outputcurrent']
    fssl=data['FsSL']
    fs=fssl[0]
    sl=fssl[1]
    mavgcurrent=np.zeros((len(gatevoltage),len(sourcevoltage)))
    mpxx1norm=np.zeros((len(gatevoltage),len(sourcevoltage)))
    mnoisepower=np.zeros((len(gatevoltage),len(sourcevoltage),int(fftlen/2+1)))
    vgi=0
    start = timeit.timeit()
    for vg in gatevoltage:
        vsi=0
        for vs in sourcevoltage:
            x=outputcurrent[vgi,vsi,:][fs:]
            f,pxx=signal.welch(x-np.average(x),fs,nperseg=fftlen,noverlap=fftoverlap)
            f1index=(np.abs(f-1)).argmin()
            pxx1norm=pxx[f1index]/np.square(np.average(x))
            mnoisepower[vgi,vsi,:]=pxx/np.square(np.average(x))
            mavgcurrent[vgi,vsi]=np.average(x)
            mpxx1norm[vgi,vsi]=pxx1norm
#            plt.semilogy(f,pxx)
#            plt.ylim([-9,-3])
#            plt.xlabel('frequency [Hz]')
#            plt.ylabel('PSD [nA^2/Hz]')
#            plt.show()
            vsi=vsi+1
        end = timeit.timeit()
        print('Time left: '+str(len(gatevoltage)*(end-start))+' seconds')
        vgi=vgi+1
    filename=pppath+'processed'+file.split('_')[0]+'.npz'
    np.savez(filename, currentdata=mavgcurrent, noise1hz=mpxx1norm, noisepower=mnoisepower, temperature=t)

directories = os.listdir(path+'/Processed/')
if len(directories)<2:
    print('Not enough temperature data points')
else:
    data1=np.load(pppath+directories[0])
    mavgcurrent1=data1['currentdata']
    mpxx1norm=data1['noise1hz']
    data2=np.load(pppath+directories[1])
    mavgcurrent2=data2['currentdata']
    tcr=(mavgcurrent1-mavgcurrent2)/(mavgcurrent1*5)
    plt.plot(sourcevoltage,mavgcurrent[6,:])
    plt.show()
    plt.loglog(f,mnoisepower[6,60,:])
    plt.show()
    