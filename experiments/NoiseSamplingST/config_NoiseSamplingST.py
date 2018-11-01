# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:43:23 2018
Config file corresponding to NoiseSamplingST.py

@author: Mark Boon
"""

from SkyNEt.config.config_class import config_class
import numpy as np


class experiment_config(config_class):
    
    
    def __init__(self):
        super().__init__()
        self.fs = 1000          # Sampling freq (Hz)
        self.sampleTime = 8     # Sampling time (s)
        self.res = 1E9
        self.steps = [[-623.79],[247.38],[826.70],[-294.96],[-108.88],[668.49],[-563.18]]  # Steps per control voltage
        self.controls = 7
        
        self.findCV = False         # If true: use GA to find CVs for all targetCurrents
        self.gridSearch = False     # If true: use a grid for sampling (use sekf.steps)
        self.T_test = True      # Tests variations in the variance for a sample time
        self.S_test = False      # Tests variations in the variance for measure - switch - measure for one CV
        self.samples = 10       # Amount of measurements for one CV config
        
        self.filepath = 'D:\\data\\Mark\\ST_tests\\'
        self.name_T = 'SampleTimeMeas' + str(self.sampleTime) +'s'
        self.name_S = 'SwitchMeas' + str(self.sampleTime) +'s'
        # [S2d, matrix module index, electrode on device]
        self.electrodeSetup = [[1,2,3,4,5,6,7,'grnd A'],[1,3,5,7,11,13,15,17],[5,6,7,8,1,2,3,4]]
        
        # IF CVs are already found, use this:
        self.CVs = np.array([[-447.703,-693.694,840.182,678.188,353.957,835.205,-783.944],
                    [-399.718,-292.205,-86.1642,900,669.22,442.349,-791.655],
                    [-726.231,69.3323,-307.257,-233.03,-45.9899,-778.111,551.091],
                    [282.338,-406.737,-379.836,189.312,-380.605,-333.847,716.212],
                    [-859.277,-819.744,-344.16,818.718,442.094,-884.256,629.337]])
                    
    
    
        #%% Use boolean logic script to find current outputs to use for noise measurement
        
        self.genelabels = ['CV1/T1','CV2/T3','CV3/T5','CV4/T7','CV5/T11','CV6/T13','CV7/T15','input scaling']
        self.nameCV = 'CVs'
        
        self.amplification = 1 
        self.genes = 8              # Must be 8 because boolean_logic defines control voltages for genes - 1
        self.genomes = 25
        self.generations = 10
        self.generange = [[-900,900], [-900, 900], [-900, 900], [-900, 900], [-900, 900], [-900, 900], [-900, 900],[0., 1.]]

        self.targetCurrent = [0.50, 1.00, 1.50, 2.00, 2.50]    # The desired output current
        self.TargetGen = self.Target
        self.Fitness = self.FitnessNMSE
        self.fitThres = 1000            #Threshold for high enough fitness value during search
              
        
    def Target(self):        # Dummy function so that the boolean_logic script can be used
        samples = 4 * round(self.fs * self.signallength / 4) + 3 * round(self.fs * self.edgelength)
        t = np.linspace(0, samples/self.fs, samples)
        x = np.zeros((len(self.targetCurrent), samples))
        for i in range(len(self.targetCurrent)):
            x[i,:] = self.targetCurrent[i] * np.ones((samples))
        return t, x
        
        
            
        
        
        
        
        

