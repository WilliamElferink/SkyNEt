import numpy as np
from SkyNEt.config.config_class import config_class
import os

class experiment_config(config_class):
    '''
    This is the config for the grid search experiment.

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
        super().__init__() #DO NOT REMOVE!
        ################################################
        ######### SPECIFY PARAMETERS ###################
        ################################################

        # Specify CVs as list of lists.
        #self.controlVoltages = [[-750, -450, -150, 0, 150, 450, 750]]*5
        #self.input2 = [-900, -600, -300, 0, 300, 600, 900]
        #self.input1 = [-900,0,900]

        self.waveElectrodes = 7

        self.factor = 4
        self.freq2 = np.array([2,np.pi,5,7,13,17,19]) 
        self.freq = np.sqrt(self.freq2[:self.waveElectrodes])*self.factor
        self.sampleTime = 53999 # Sample time of the sine waves for one grid point (in seconds)

        self.fs = 1000
        self.transientTest = True
        self.n = 200
        
        # If the input data is too large for RAM, load the data in small parts
        self.loadData = True
        self.loadPoints = 10000
        self.loadString = r'D:\data\Mark\wave_search\inputData.npz'
        
        self.amplification = 1000
        self.postgain = 100
        self.Vmax = 0.8 # Maximum amount of voltage for the inputs

        self.keithley_address = 'GPIB0::17::INSTR'

        #                               Summing module S2d      Matrix module           device
        self.electrodeSetup = [['ao0','ao2','ao4''ao6','a05','ao3','ao1','out'],[1,3,5,7,11,13,15,17],[5,6,7,8,1,2,3,4]]
        # Save settings
        self.filepath = r'D:\\data\\Mark\\wave_search\\'
        self.name = 'test_7_waves_factor_'+str(self.factor) + 'sampleTime_' + str(self.sampleTime) + 's_loaded'
        self.configSrc = os.path.dirname(os.path.abspath(__file__))
        
        
        self.t = np.arange(0, self.sampleTime, 1/self.fs)
        self.phase = 2*np.pi*np.random.rand(self.waveElectrodes,1)

    #####################################################
    ############# USER-SPECIFIC METHODS #################
    #####################################################
    # Optionally define new methods here that you wish to use in your experiment.
    # These can be e.g. new fitness functions or input/output generators.

