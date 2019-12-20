import time
import numpy as np
import itertools
import matplotlib.pyplot as plt
import time
from instruments.ADwin import adwinIO

pulseamount2 = 5
offset = 0
amplification = 0.5
samplefrequency = 1000
plateapoints = 5
slopepoints = 10
numberinputs = (plateapoints+slopepoints)*3
Sourcegain = 5

a = [0, 1]
c = [1]
d = [0]
win = np.array(list(itertools.product(*[d,c,d])))
singlepuls = np.zeros(numberinputs)

# print(win)
output = np.zeros(numberinputs)
axis = np.linspace(1, 225, 225)
# print(np.shape(win)[1])
slopeup = np.linspace(0, 1, slopepoints)
slopedown = np.linspace(1, 0, slopepoints)
ax5 = np.linspace(1,45,45)
# print(slopeup)
# print(slopedown)

cornerdistance = plateapoints+slopepoints

adwin = adwinIO.initInstrument() 
for pulseamount in range(pulseamount2):

    for i in range(len(win)):
        for j in range(np.shape(win)[1]-1):

            if win[i,j] == 0 and win[i,j+1] == 0:
                singlepuls[cornerdistance*j:cornerdistance*j+cornerdistance]= win[i,j]

            elif win[i,j] == 0 and win[i,j+1] == 1:
                singlepuls[cornerdistance*j:cornerdistance*j+plateapoints] = win[i,j]
                singlepuls[cornerdistance*j+plateapoints:cornerdistance*j+cornerdistance] = slopeup

            elif win[i,j] == 1 and win[i,j+1] == 1:
        	    singlepuls[cornerdistance*j:cornerdistance*j+cornerdistance]= win[i,j]

            elif win[i,j] == 1 and win[i,j+1] == 0:
                singlepuls[cornerdistance*j:cornerdistance*j+plateapoints] = win[i,j]
                singlepuls[cornerdistance*j+plateapoints:cornerdistance*j+cornerdistance] = slopedown

        if win[i,0] == 1:
    	    singlepuls[0:slopepoints] = slopeup


    adwininput = [0]
    scaledsinglepulse = (singlepuls*amplification)/Sourcegain
    for n in range(pulseamount):
        

        adwininput[n*len(scaledsinglepulse):n*len(scaledsinglepulse)+len(scaledsinglepulse)] = scaledsinglepulse+offset


    axis = np.linspace(1,pulseamount*45,pulseamount*45)
    # plt.figure()
    # plt.plot(axis, adwininput)
    # plt.show()
    if pulseamount == 0:
        axis = [0]


    # plt.figure()
    # plt.plot(axis2, adwininput)
    # plt.show()

    x = adwinIO.IO(adwin, adwininput, samplefrequency)
    adwininput = []
    # plt.figure()
    # plt.plot(axis, x)
    # plt.show()

    Input = np.array([0.01,0.01,0.01])/Sourcegain
    # output[pulseamount:pulseamount+3] = np.average(adwinIO.IO(adwin, Input, samplefrequency))
    output = np.array(output)
    time.sleep(5)


fig, (ax1) = plt.subplots(1,1)
ax1.plot(ax5, output[0:49])
plt.show()

datetime = time.strftime("%Y_%m_%d_%H%M%S")
np.savetxt('D:/data/Bram/Pulse/'+datetime+'pulse.txt', (output[0:pulseamount2]),x)