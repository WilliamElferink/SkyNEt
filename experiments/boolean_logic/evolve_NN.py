'''
This is a template for evolving the NN based on the boolean_logic experiment. 
The only difference to the measurement scripts are on lines where the device is called.

'''
# SkyNEt imports
import SkyNEt.modules.SaveLib as SaveLib
import SkyNEt.modules.Evolution as Evolution
import SkyNEt.modules.PlotBuilder as PlotBuilder
import config_evolve_NN as config
from SkyNEt.modules.Nets.staNNet import staNNet 
# Other imports
import torch
from torch.autograd import Variable
import time
import numpy as np

#%% Initialization

# Initialize config object
cf = config.experiment_config()

# Initialize input and target
t = cf.InputGen()[0]  # Time array
x = np.asarray(cf.InputGen()[1:3])  # Array with P and Q signal
w = cf.InputGen()[3]  # Weight array
target = cf.TargetGen()[1]  # Target signal

# np arrays to save genePools, outputs and fitness
geneArray = np.zeros((cf.generations, cf.genomes, cf.genes))
outputArray = np.zeros((cf.generations, cf.genomes, len(x[0])))
fitnessArray = np.zeros((cf.generations, cf.genomes))

# Temporary arrays, overwritten each generation
fitnessTemp = np.zeros((cf.genomes, cf.fitnessavg))
outputAvg = np.zeros((cf.fitnessavg, len(x[0])))
outputTemp = np.zeros((cf.genomes, len(x[0])))
#controlVoltages = np.zeros(cf.genes)

# Initialize save directory
saveDirectory = SaveLib.createSaveDirectory(cf.filepath, cf.name)

## Initialize main figure
mainFig = PlotBuilder.initMainFigEvolution(cf.genes, cf.generations, cf.genelabels, cf.generange)

# Initialize NN
main_dir = r'../../test/NN_test/data4nn/Data_for_testing/'
dtype = torch.FloatTensor
#Note: this is an old NN for which I dont remember the specific ranges. But they are approx the same as indicated in the cong_evolve_NN file. 
#possibly the generange for this NN is 0.2 V or so smaller. 
net = staNNet(main_dir+'NN_New.pt')

# Initialize genepool
genePool = Evolution.GenePool(cf)

#%% Measurement loop

for i in range(cf.generations):
    start = time.time()
   
    for j in range(cf.genomes):
        # Set the DAC voltages
#        for k in range(cf.genes-1):
#            controlVoltages[k] = genePool.MapGenes(
#                                    cf.generange[k], genePool.pool[j, k])
        #Set the input scaling 
        x_scaled = x * genePool.pool[j,-1]
       
        # Measure cf.fitnessavg times the current configuration
        for avgIndex in range(cf.fitnessavg):
            # Feed input to NN
            
            #You only want to feed the control voltages and the input (remove input scaling)
            
            #Change: 
            #Note: self.input_electrodes = [1,2]. This can be adapted in the config_evolve_NN file 
            g = np.ones_like(target)[:,np.newaxis]*genePool.pool[j,:-1][:,np.newaxis].T
            
            x_dummy = np.insert(g, cf.input_electrodes[0], x_scaled.T[:,0],axis=1)
            x_dummy = np.insert(x_dummy, cf.input_electrodes[1], x_scaled.T[:,1],axis=1)

            inputs = torch.from_numpy(x_dummy).type(dtype)
            inputs = Variable(inputs)
            output = net.outputs(inputs) * cf.amplification 


#            # Plot genome
            PlotBuilder.currentGenomeEvolution(mainFig, genePool.pool[j])

            # Train output
            #Change: amplification is moved to line 84
            outputAvg[avgIndex] = np.asarray(output)  # empty for now, as we have only one output node

            # Calculate fitness
            # Change: forward the clipping value to the fitness function (before it was hardcoded in the fitness function)
            fitnessTemp[j, avgIndex]= cf.Fitness(outputAvg[avgIndex],
                                                     target,
                                                     w, cf.clpval)
#           # Plot output
            #Change: forward the clipping value to the plot builder 
            PlotBuilder.currentOutputEvolution(mainFig,
                                               t,
                                               target,
                                               output,
                                               j + 1, i + 1,
                                               fitnessTemp[j, avgIndex], cf.clpval)
        outputTemp[j] = outputAvg[np.argmin(fitnessTemp[j])]

    genePool.fitness = fitnessTemp.min(1)  # Save fitness
    end = time.time()
    # Status print
    print("Generation nr. " + str(i + 1) + " completed; took "+str(end-start)+" sec.")
    print("Highest fitness: " + str(max(genePool.fitness)))

    # Save generation data
    geneArray[i, :, :] = genePool.pool
    outputArray[i, :, :] = outputTemp
    fitnessArray[i, :] = genePool.fitness

    # Update main figure
    PlotBuilder.updateMainFigEvolution(mainFig,
                                       geneArray,
                                       fitnessArray,
                                       outputArray,
                                       i + 1,
                                       t,
                                       cf.amplification*target,
                                       output,
                                       w)

    # Save generation
    SaveLib.saveExperiment(saveDirectory,
                           genes = geneArray,
                           output = outputArray,
                           fitness = fitnessArray)

    # Evolve to the next generation
    genePool.NextGen()

PlotBuilder.finalMain(mainFig)