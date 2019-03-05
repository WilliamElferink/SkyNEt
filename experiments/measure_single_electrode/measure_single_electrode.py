'''
This script applies control+input voltage configurations defined in the
config file. One of these voltages is applied with the Keithley2400,
such that the current through this electrode can be measured.
By performing this measurement 7 times (all electrodes but the output),
all flowing currents in a particular configuration can be indexed.
'''
# SkyNEt imports
import SkyNEt.modules.SaveLib as SaveLib
import config_measure_single_electrode as config
from SkyNEt.instruments import InstrumentImporter
from SkyNEt.instruments.Keithley2400 import Keithley2400

# Other imports
import time
import numpy as np

# Initialize config object
cf = config.experiment_config()

# Initialize save directory
saveDirectory = SaveLib.createSaveDirectory(cf.filepath, cf.name)

# Initialize instruments
ivvi = InstrumentImporter.IVVIrack.initInstrument()
keithley = Keithley2400.Keithley_2400('keithley', 'GPIB0::11')

# Set compliances
keithley.compliancei.set(1E-6)
keithley.compliancev.set(4)

P = [0, 1, 0, 1]
Q = [0, 0, 1, 1]
for ii in range(cf.control_sequence.shape[0]):
    controlVoltages = cf.control_sequence[ii].copy()
    input_output = np.zeros((4, 8))  # Each row is control sequence + measured current
    waveform = np.zeros((4, cf.N))
    for jj in range(4):
        # Prepare controlVoltages
        controlVoltages[0] = P[jj]*cf.control_sequence[ii, 0]
        controlVoltages[1] = Q[jj]*cf.control_sequence[ii, 1]

        # Set the DAC voltages
        InstrumentImporter.IVVIrack.setControlVoltages(ivvi, controlVoltages)
        time.sleep(.1)  # Wait after setting DACs

        # Apply Keithley input
        keithley.output.set(1)
        keithley.volt.set(controlVoltages[cf.measure_electrode])
        time.sleep(.1)

        # Measure N datapoints
        for kk in range(cf.N):
            waveform[jj] = keithley.curr()
            time.sleep(cf.wait_time)

        # Store result in input_output
        input_output[jj, :7] = controlVoltages
        input_output[jj, 7] = np.mean(waveform)

    keithley.output.set(0)

    # Save experiment
    SaveLib.saveExperiment(saveDirectory,
                           input_output = input_output,
                           waveform = waveform,
                           measure_electrode = cf.measure_electrode
                           )

InstrumentImporter.reset(0, 0)
