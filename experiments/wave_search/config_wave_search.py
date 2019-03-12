import numpy as np
from SkyNEt.config.config_class import config_class
import os

class experiment_config(config_class):
    '''
    This is the config for the wave search experiment. The input waves are generated by generateSineWave
    which can be configured with the parameters below. The input data is not saved in the experiment file
    (and also not in the RAM) since this takes up too much space. 

    Warning: the  ao and ai slowly get out of sync on the cDAQ so it is best to sample data in small batches. It is not
    consistent when they get out of sync, but it is advised to stay at least below batches of 25 seconds so 
    that the input/output mismatch is at most 1 datapoint.

    ----------------------------------------------------------------------------
    Description of general parameters
    ----------------------------------------------------------------------------
    filepath = 'D:\data\data4nn'
    name = 'FullSwipe_TEST'
    controlVoltages = [[-900, -600, -300, 0, 300, 600, 900]]*5
    input2 = [-900, -600, -300, 0, 300, 600, 900]
    input1 = [-900,0,900]
    voltageGrid = [*controlVoltages,input2,input1]
    electrodes = len(voltageGrid) #amount of electrodes
    acqTime = 0.01
    samples = 50

    '''

    def __init__(self):
        super().__init__() 

        self.waveElectrodes = 7
        self.factor = 1
        self.freq2 = np.array([2,np.pi,5,7,13,17,19]) 
        self.freq = np.sqrt(self.freq2[:self.waveElectrodes])*self.factor
        self.phase = np.zeros(self.waveElectrodes)
        self.sampleTime = 50 # Sample time of the sine waves for one grid point (in seconds)
        self.fs = 1000
        self.transientTest = True
        self.n = 50 # Amount of test points for the transient test
        self.samplePoints = 50*1000 # Amount of sample points per batch measurement (sampleTime*fs/samplePoints batches)
        self.amplification = 1000
        self.postgain = 100
        self.amplitude = 0.6 # Maximum amount of voltage for the inputs
        self.offset = np.zeros(self.waveElectrodes) # Optional offset for the sine waves

        self.keithley_address = 'GPIB0::17::INSTR'
        #                               Summing module S2d      Matrix module           device
        self.electrodeSetup = [['ao0','ao2','ao4''ao6','a05','ao3','ao1','out'],[1,3,5,7,11,13,15,17],[5,6,7,8,1,2,3,4]]
        # Save settings
        self.filepath = r'D:\\data\\Mark\\wave_search\\'
        #self.name = 'wave_search_f'+str(self.factor) + 'sampleTime_' + str(int(self.sampleTime)) + 's_loadEvery_' + str(int(self.loadPoints/self.fs)) + 's'
        self.name = 'speedTest_factor_' + str(self.factor) + '_T_' + str(self.sampleTime) + 's_batch_' + str(int(self.samplePoints/self.fs)) + 's'
        self.configSrc = os.path.dirname(os.path.abspath(__file__))
        
        self.inputData = self.generateSineWave




    def generateSineWave(self, freq, t, amplitude, fs, phase = np.zeros(7)):
        '''
        Generates a sine wave that can be used for the input data.

        freq:       Frequencies of the inputs in an one-dimensional array
        t:          The datapoint(s) index where to generate a sine value (1D array when multiple datapoints are used)
        amplitude:  Amplitude of the sine wave (Vmax in this case)
        fs:         Sample frequency of the device
        phase:      (Optional) phase offset at t=0
        '''

        return np.sin((2 * np.pi * freq[:, np.newaxis] * t + phase[:,np.newaxis])/ fs) * amplitude