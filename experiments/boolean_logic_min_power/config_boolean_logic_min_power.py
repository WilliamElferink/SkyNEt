import numpy as np
from SkyNEt.config.config_class import config_class

class experiment_config(config_class):
    '''This is the experiment configuration file for the boolean logic experiment.
    It also serves as a template for other experiments, so please model your work
    after this when you make new experiments.
    This experiment_config class inherits from config_class default values that are known to work well with boolean logic.
    You can define user-specific parameters in the construction of the object in __init__() or define
    methods that you might need after, e.g. a new fitness function or input and output generators.
    Remember if you define a new fitness function or generator, you have to redefine the self.Fitness,
    self.Target_gen and self.Input_gen in __init__()

    ----------------------------------------------------------------------------
    Description of general parameters
    ----------------------------------------------------------------------------
    comport; the COM port to which the ivvi rack is connected.
    amplification; specify the amount of nA/V. E.g. if you set the IVVI to 100M,
        then amplification = 10
    generations; the amount of generations for the GA
    generange; the range that each gene ([0, 1]) is mapped to. E.g. in the Boolean
        experiment the genes for the control voltages are mapped to the desired
        control voltage range.
    partition; this tells the GA how it will evolve the next generation.
        In order, this will make the GA evolve the specified number with
        - promoting fittest partition[0] genomes unchanged
        - adding Gaussian noise to the fittest partition[1] genomes
        - crossover between fittest partition[2] genomes
        - crossover between fittest partition[3] and randomly selected genes
        - randomly adding parition[4] genomes
    genomes; the amount of genomes in the genepool, speficy this parameter instead
        of partition if you don't care about the specific partition.
    genes; the amount of genes per genome
    mutationrate; the probability of mutation for each gene (between 0 and 1)
    fitnessavg; the amount of times the same genome is tested to obtain the fitness
        value.
    fitnessparameters; the parameters for FitnessEvolution (see its doc for
        specifics)
    filepath; the path used for saving your experiment data
    name; name used for experiment data file (date/time will be appended)

    ----------------------------------------------------------------------------
    Description of method parameters
    ----------------------------------------------------------------------------
    signallength; the length in s of the Boolean P and Q signals
    edgelength; the length in s of the edge between 0 and 1 in P and Q
    fs; sample frequency for niDAQ or ADwin

    ----------------------------------------------------------------------------
    Description of methods
    ----------------------------------------------------------------------------
    TargetGen; specify the target function you wish to evolve, options are:
        - OR
        - AND
        - NOR
        - NAND
        - XOR
        - XNOR
    Fitness; specify the fitness function, standard options are:
        - FitnessEvolution; standard fitness used for boolean logic
        - FitnessNMSE; normalised mean squared error
    '''

    def __init__(self):
        super().__init__() #DO NOT REMOVE!
        ################################################
        ######### SPECIFY PARAMETERS ###################
        ################################################
        self.comport = 'COM3'  # COM port for the ivvi rack
        self.device = 'nidaq'  # Either nidaq or adwin

        # Define experiment
        self.amplification = 10  # nA/V
        self.TargetGen = self.OR
        self.generations = 100
        self.generange = [[-1000,500], [-1300, 900], [-1300, 900], [-1300, 900], [-1000, 500], [0.01, 1]]
        self.resistance = 150E3  # Ohm
        self.P_target = 1E-7  # W
        self.P_max = 35E-6
        self.separation_treshold = 2E-9
        self.pcc_treshold = 0.75
        self.current_resolution = 10E-9
        self.edgelength = 0.2
        self.signallength = 1
        self.plot_flag = False
        self.fitnessavg = 3

        # Specify either partition or genomes
        #self.partition = [5, 5, 5, 5, 5]
        self.genomes = 25
        self.Fitness = self.FitnessPower5
        # Documentation
        self.genelabels = ['CV1/T11','CV2/T13','CV3/T17','CV4/T7','CV5/T1', 'Input scaling']

        # Save settings
        self.filepath = r'D:\Data\BramdW\D9\power_min_multiply_fitness\\'  #Important: end path with double backslash
        self.name = 'OR_150e3'

        ################################################
        ################# OFF-LIMITS ###################
        ################################################
        # Check if genomes parameter has been changed
        if(self.genomes != sum(self.default_partition)):
            if(self.genomes%5 == 0):
                self.partition = [int(self.genomes/5)]*5  # Construct equally partitioned genomes
            else:
                print('WARNING: The specified number of genomes is not divisible by 5.'
                      + ' The remaining genomes are generated randomly each generation. '
                      + ' Specify partition in the config instead of genomes if you do not want this.')
                self.partition = [self.genomes//5]*5  # Construct equally partitioned genomes
                self.partition[-1] += self.genomes%5  # Add remainder to last entry of partition

        self.genomes = int(sum(self.partition))  # Make sure genomes parameter is correct
        self.genes = int(len(self.generange))  # Make sure genes parameter is correct

    #####################################################
    ############# USER-SPECIFIC METHODS #################
    #####################################################
    # Optionally define new methods here that you wish to use in your experiment.
    # These can be e.g. new fitness functions or input/output generators.

    def FitnessPower(self, I, V, target, w, P_max):
        '''
        This fitness function attempts to minimize total power consumption.

        Assumes both I and V vectors have consisent units!
        '''
        # Apply weights w
        indices = np.argwhere(w)  #indices where w is nonzero (i.e. 1)

        I_weighed = np.zeros((8, len(indices)))
        V_weighed = np.zeros((8, len(indices)))
        target_weighed = np.zeros(len(indices))
        for i in range(len(indices)):
                I_weighed[:, i] = I[:, indices[i][0]]
                V_weighed[:, i] = V[:, indices[i][0]]
                target_weighed[i] = target[indices[i][0]]

        # Get correlation
        corr = np.corrcoef(I_weighed[7], target_weighed)[0, 1]

        # Get average currents per input configuration
        I_avg = np.zeros((8, 4))
        V_avg = np.zeros((8, 4))
        blocksize = len(target_weighed)//4
        for i in range(4):
            I_avg[:, i] = np.mean(I_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            V_avg[:, i] = np.mean(V_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)

        # Calculate power for each input configuration
        P = np.zeros(4)
        for i in range(4):
            P[i] = np.sum(I_avg[:7, i]*V_avg[:7, i])

        # Calculate average power
        P_avg = np.abs(np.mean(P))

        # Check for clipping
        clipped = False
        for i in range(len(indices)):
            if(abs(I_weighed[7,i]) > 3.3E-9*self.amplification):
                clipped = True
                break
                
        # Calculate final fitness
        if(clipped):
            return -100
        elif((1-P_avg/P_max) < 0 and corr < 0):
            return -(1 - P_avg/P_max)*corr
        else:
            return (1 - P_avg/P_max)*corr

    def FitnessPower2(self, I, V, target, w, P_max):
        '''
        This fitness function attempts to minimize total power consumption.

        Assumes both I and V vectors have consisent units!
        '''
        # Apply weights w
        indices = np.argwhere(w)  #indices where w is nonzero (i.e. 1)

        I_weighed = np.zeros((8, len(indices)))
        V_weighed = np.zeros((8, len(indices)))
        target_weighed = np.zeros(len(indices))
        for i in range(len(indices)):
            I_weighed[:, i] = I[:, indices[i][0]]
            V_weighed[:, i] = V[:, indices[i][0]]
            target_weighed[i] = target[indices[i][0]]

        # Determine normalized separation
        indices1 = np.argwhere(target_weighed)  #all indices where target is nonzero
        x0 = np.empty(0)  #list of values where x should be 0
        x1 = np.empty(0)  #list of values where x should be 1
        for i in range(len(target_weighed)):
            if(i in indices1):
                x1 = np.append(x1, I_weighed[7, i])
            else:
                x0 = np.append(x0, I_weighed[7, i])
        Q = (min(x1) - max(x0)) / (self.separation_treshold)

        # Get average currents per input configuration
        I_avg = np.zeros((8, 4))
        V_avg = np.zeros((8, 4))
        blocksize = len(target_weighed)//4
        for i in range(4):
            I_avg[:, i] = np.mean(I_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            V_avg[:, i] = np.mean(V_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)

        # Calculate power for each input configuration
        P = np.zeros(4)
        for i in range(4):
            P[i] = np.sum(I_avg[:7, i]*V_avg[:7, i])

        # Calculate average power
        P_avg = np.abs(np.mean(P))

        # Check for clipping
        clipped = False
        for i in range(len(indices)):
            if(abs(I_weighed[7,i]) > 3.3E-9*self.amplification):
                clipped = True
                return -100

        # Return final fitness
        if(Q < 1):
            return Q
        else:
            return 1 + 1/P_avg

    def FitnessPower3(self, I, V, target, w):
        '''
        This fitness function attempts to minimize total power consumption.

        It is a three stage fitness, using correlation, separation
        and power consumption:

        Stage 1: PCC-2:  number between -3 and -1
        Stage 2: Separation/tresh:  number between -range and range,
            if it is 1 target separation has been achieved.
        Stage 3: 1 + P_target/P_avg

        Return stage 1 if PCC < 0.8
        Return stage 2 if separation/tresh < 1
        Return stage 3 
        '''
        # Apply weights w
        indices = np.argwhere(w)  #indices where w is nonzero (i.e. 1)

        I_weighed = np.zeros((8, len(indices)))
        V_weighed = np.zeros((8, len(indices)))
        target_weighed = np.zeros(len(indices))
        for i in range(len(indices)):
            I_weighed[:, i] = I[:, indices[i][0]]
            V_weighed[:, i] = V[:, indices[i][0]]
            target_weighed[i] = target[indices[i][0]]

        # Determine PCC
        pcc = np.corrcoef(I_weighed[7], target_weighed)[0, 1]

        # Determine normalized separation
        indices1 = np.argwhere(target_weighed)  #all indices where target is nonzero
        x0 = np.empty(0)  #list of values where x should be 0
        x1 = np.empty(0)  #list of values where x should be 1
        for i in range(len(target_weighed)):
            if(i in indices1):
                x1 = np.append(x1, I_weighed[7, i])
            else:
                x0 = np.append(x0, I_weighed[7, i])
        Q = (min(x1) - max(x0)) / (self.separation_treshold)

        # Get average currents per input configuration
        I_avg = np.zeros((8, 4))
        V_avg = np.zeros((8, 4))
        blocksize = len(target_weighed)//4
        for i in range(4):
            I_avg[:, i] = np.mean(I_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            V_avg[:, i] = np.mean(V_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            
        # Cap current if it is within current resolution
        for i in range(7):
            for j in range(4):
                if(abs(I_avg[i, j]) < self.current_resolution):
                    I_avg[i, j] = np.sign(I_avg[i, j]) * self.current_resolution
                    

        # Calculate power for each input configuration
        P = np.zeros(4)
        for i in range(4):
            P[i] = np.sum(I_avg[:7, i]*V_avg[:7, i])

        # Calculate average power
        P_avg = np.abs(np.mean(P))

        # Check for clipping
        clipped = False
        for i in range(len(indices)):
            if(abs(I_weighed[7,i]) > 3.3E-9*self.amplification):
                clipped = True
                return -100

        # Return final fitness
        if(pcc < self.pcc_treshold and Q < 0):
            return pcc-2
        elif(Q < 1):
            return Q
        else:
            return 1 + self.P_target/P_avg
            
    def FitnessPower4(self, I, V, target, w):
        '''
        This fitness function attempts to minimize total power consumption.

        It is a three stage fitness, using correlation, separation
        and power consumption:

        Stage 1: PCC-3:  number between -4 and -2
        Stage 2: Separation/range-1:  number between -2 and 0,
        Stage 3: P_target/P_avg

        Return stage 1 if PCC < pcc_treshold
        Return stage 2 if separation < separation_treshold
        Return stage 3 
        
        Some indicators:
        F > -2; target correlation achieved
        F > 0; target separation achieved, i.e. valid gate
        F > 1; valid gate with target power consumption
        '''
        # Apply weights w
        indices = np.argwhere(w)  #indices where w is nonzero (i.e. 1)

        I_weighed = np.zeros((8, len(indices)))
        V_weighed = np.zeros((8, len(indices)))
        target_weighed = np.zeros(len(indices))
        for i in range(len(indices)):
            I_weighed[:, i] = I[:, indices[i][0]]
            V_weighed[:, i] = V[:, indices[i][0]]
            target_weighed[i] = target[indices[i][0]]

        # Determine PCC
        pcc = np.corrcoef(I_weighed[7], target_weighed)[0, 1]

        # Determine normalized separation
        indices1 = np.argwhere(target_weighed)  #all indices where target is nonzero
        x0 = np.empty(0)  #list of values where x should be 0
        x1 = np.empty(0)  #list of values where x should be 1
        for i in range(len(target_weighed)):
            if(i in indices1):
                x1 = np.append(x1, I_weighed[7, i])
            else:
                x0 = np.append(x0, I_weighed[7, i])
        Q = (min(x1) - max(x0))

        # Get average currents per input configuration
        I_avg = np.zeros((8, 4))
        V_avg = np.zeros((8, 4))
        blocksize = len(target_weighed)//4
        for i in range(4):
            I_avg[:, i] = np.mean(I_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            V_avg[:, i] = np.mean(V_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            
        # Cap current if it is within current resolution
        for i in range(7):
            for j in range(4):
                if(abs(I_avg[i, j]) < self.current_resolution):
                    I_avg[i, j] = np.sign(I_avg[i, j]) * self.current_resolution
                    

        # Calculate power for each input configuration
        P = np.zeros(4)
        for i in range(4):
            P[i] = np.sum(I_avg[:7, i]*V_avg[:7, i])

        # Calculate average power
        P_avg = np.abs(np.mean(P))

        # Check for clipping
        clipped = False
        for i in range(len(indices)):
            if(abs(I_weighed[7,i]) > 3.3E-9*self.amplification):
                clipped = True
                return -100

        # Return final fitness
        if(pcc < self.pcc_treshold):
            return pcc-3
        elif(Q < self.separation_treshold):
            return Q/(6.6E-9*self.amplification) - 1
        else:
            return self.P_target/P_avg
            
    def FitnessPower5(self, I, V, target, w):
        '''
        This fitness function attempts to minimize total power consumption.

        It is a three stage fitness, using correlation, separation
        and power consumption:

        Stage 1: PCC-3:  number between -4 and -2
        Stage 2: Separation/range-1:  number between -2 and 0,
        Stage 3: P_target/P_avg

        Return stage 1 if PCC < pcc_treshold
        Return stage 2 if separation < separation_treshold
        Return stage 3 
        
        Some indicators:
        F > -2; target correlation achieved
        F > 0; target separation achieved, i.e. valid gate
        F > 1; valid gate with target power consumption
        '''
        # Apply weights w
        indices = np.argwhere(w)  #indices where w is nonzero (i.e. 1)

        I_weighed = np.zeros((8, len(indices)))
        V_weighed = np.zeros((8, len(indices)))
        target_weighed = np.zeros(len(indices))
        for i in range(len(indices)):
            I_weighed[:, i] = I[:, indices[i][0]]
            V_weighed[:, i] = V[:, indices[i][0]]
            target_weighed[i] = target[indices[i][0]]

        # Determine PCC
        pcc = np.corrcoef(I_weighed[7], target_weighed)[0, 1]

        # Determine normalized separation
        indices1 = np.argwhere(target_weighed)  #all indices where target is nonzero
        x0 = np.empty(0)  #list of values where x should be 0
        x1 = np.empty(0)  #list of values where x should be 1
        for i in range(len(target_weighed)):
            if(i in indices1):
                x1 = np.append(x1, I_weighed[7, i])
            else:
                x0 = np.append(x0, I_weighed[7, i])
        Q = (min(x1) - max(x0))

        # Get average currents per input configuration
        I_avg = np.zeros((8, 4))
        V_avg = np.zeros((8, 4))
        blocksize = len(target_weighed)//4
        for i in range(4):
            I_avg[:, i] = np.mean(I_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            V_avg[:, i] = np.mean(V_weighed[:, i*blocksize:(i+1)*blocksize], axis=1)
            
        # Cap current if it is within current resolution
        for i in range(7):
            for j in range(4):
                if(abs(I_avg[i, j]) < self.current_resolution):
                    I_avg[i, j] = np.sign(I_avg[i, j]) * self.current_resolution
                    

        # Calculate power for each input configuration
        P = np.zeros(4)
        for i in range(4):
            P[i] = np.sum(I_avg[:7, i]*V_avg[:7, i])

        # Calculate average power
        P_avg = np.abs(np.mean(P))

        # Check for clipping
        clipped = False
        for i in range(len(indices)):
            if(abs(I_weighed[7,i]) > 3.3E-9*self.amplification):
                clipped = True
                return -100

        # Return final fitness
        if(pcc < 0):
            return pcc
        else:
            return (1 - P_avg/self.P_max)**3*pcc


    def FitnessEvolution(self, x, target, W):
        '''
        This implements the fitness function
        F = self.fitnessparameters[0] * m / (sqrt(r) + self.fitnessparameters[3] * abs(c)) + self.fitnessparameters[1] / r + self.fitnessparameters[2] * Q
        where m,c,r follow from fitting x = m*target + c to minimize r
        and Q is the fitness quality as defined by Celestine in his thesis
        appendix 9
        W is a weight array consisting of 0s and 1s with equal length to x and
        target. Points where W = 0 are not included in fitting.
        '''

        #extract fit data with weights W
        indices = np.argwhere(W)  #indices where W is nonzero (i.e. 1)

        x_weighed = np.empty(len(indices))
        target_weighed = np.empty(len(indices))
        for i in range(len(indices)):
        	x_weighed[i] = x[indices[i]]
        	target_weighed[i] = target[indices[i]]


    	#fit x = m * target + c to minimize res
        A = np.vstack([target_weighed, np.ones(len(indices))]).T  #write x = m*target + c as x = A*(m, c)
        m, c = np.linalg.lstsq(A, x_weighed)[0]
        res = np.linalg.lstsq(A, x_weighed)[1]
        res = res[0]

        #determine fitness quality
        indices1 = np.argwhere(target_weighed)  #all indices where target is nonzero
        x0 = np.empty(0)  #list of values where x should be 0
        x1 = np.empty(0)  #list of values where x should be 1
        for i in range(len(target_weighed)):
            if(i in indices1):
                x1 = np.append(x1, x_weighed[i])
            else:
                x0 = np.append(x0, x_weighed[i])
        if(min(x1) < max(x0)):
            Q = 0
        else:
            Q = (min(x1) - max(x0)) / (max(x1) - min(x0) + abs(min(x0)))

        F = self.fitnessparameters[0] * m / (res**(.5) + self.fitnessparameters[3] * abs(c)) + self.fitnessparameters[1] / res + self.fitnessparameters[2] * Q
        clipcounter = 0
        for i in range(len(x_weighed)):
            if(abs(x_weighed[i]) > 3.1*10):
                clipcounter = clipcounter + 1
                F = -100
        return F
