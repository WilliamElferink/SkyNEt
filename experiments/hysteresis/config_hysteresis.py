import numpy as np
from SkyNEt.config.config_class import config_class
import os

class experiment_config(config_class):
    '''
    This is the config for the wave search experiment. The input waves are generated by generateSineWave
    which can be configured with the parameters below. The input data is not saved in the experiment file
    (and also not in the RAM) since this takes up too much space. 
    
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
        self.factor = 0.05
        self.freq2 = np.array([2,np.pi,5,7,13,17,19]) 
        self.freq = np.sqrt(self.freq2[:self.waveElectrodes])*self.factor
        self.phase = np.zeros(self.waveElectrodes)
        self.sampleTime = 150 # Sample time of the sine waves for one grid point (in seconds)
        self.fs = 50
        self.nr_halfloops = 10 #
        self.samplePoints = int(150*self.fs) # Amount of sample points per batch measurement (sampleTime*fs/samplePoints batches)
        self.amplification = 100
        self.gain_info = '10MV/A'
        self.postgain = 1
        self.amplitude = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.5, 0.5]) # Maximum amount of voltage for the inputs
        self.offset = np.array([-0.3,-0.3,-0.3,-0.3,-0.3,-0.2,-0.2]) # Optional offset for the sine waves

        self.keithley_address = 'GPIB0::17::INSTR'
        #                               Summing module S2d      Matrix module           device
        self.electrodeSetup = [['ao5','ao3','ao1''ao0','a02','ao4','ao6','out'],[1,3,5,6,11,13,15,17],[5,6,7,8,1,2,3,4]]

        # Save settings
        self.filepath = r'D:\data\Mark\hysteresis\paper_chip\\'
        
        self.name = 'hysteresis_150s_f_0_05'

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

        return np.sin((2 * np.pi * freq[:, np.newaxis] * t)/ fs + phase[:,np.newaxis]) * amplitude[:,np.newaxis]