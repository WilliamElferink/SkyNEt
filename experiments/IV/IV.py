import SkyNEt.modules.SaveLib as SaveLib
import matplotlib.pyplot as plt
from SkyNEt.instruments import InstrumentImporter
import numpy as np
import os
import config_IV as config

# Load the information from the config class.
config = config.experiment_config()

# Initialize save directory.
saveDirectory = SaveLib.createSaveDirectory(config.filepath, config.name)

# Define the device input using the function in the config class.

Input = config.Sweepgen( config.v_high, config.v_low, config.n_points,config.backgate, config.direction)
#Input = np.zeros([2, config.n_points])
##Input = config.Pulse(config.v_high, config.v_low, config.n_points, config.n_pulses)
#Input = config.sine(config.n_points, 1, config.v_high)
# Measure using the device specified in the config class.
if config.device == 'nidaq':
    Output = InstrumentImporter.nidaqIO.IO_cDAQ9132(Input, config.fs)
elif config.device == 'adwin':
    adwin = InstrumentImporter.adwinIO.initInstrument()
    Output = InstrumentImporter.adwinIO.IO(adwin, Input, config.fs)
else:
    print('specify measurement device')

# Save the Input and Output
#SaveLib.saveExperiment(config.configSrc, saveDirectory, input = Input, output = Output)
#print(Input)
#print(Output)
# Final reset
#InstrumentImporter.reset(0, 0)
#N  = np.linspace(0,1,len(Output[0]))
#calculate resistance ONLY USE IF LINEAR
# watch out, beun
#resistance = np.zeros(int(len(Input[0])/50)-1)
#for i in range(1,int(len(Input[0])/50)):
#    resistance[i-1] = Input[0,50*i+2]/Output[0,50*i+2]
#avgresistance = np.average(resistance)*100e6 # 100e6 is the amplification
#print(resistance)
#print('the resistance is %i ohms' %avgresistance)
# Plot the IV curve.
plt.figure()
plt.plot(Input[0], Output[0])
#plt.title('device measurement')#average R = %i' %avgresistance)
plt.xlabel('voltage (V)')
plt.ylabel('current (10nA)')
plt.show()

# Final reset
InstrumentImporter.reset(0, 0)
# Since InstrumentImporter is not working properly, use adwin reset directly: OLD?

