'''This test is for testing the Evolution module. The fitness function is
1/(1 + y.T*y), where y is a genome. In other words, the GA should arrive at
(unique) optimal solution y=0 with fitness = 1'''

import numpy as np
import matplotlib.pyplot as plt
import config_evolution_test as cf
import SkyNEt.modules.Evolution as evo

# Initialize config object
conf_obj = cf.experiment_config()

# Initialize genepool
pool = evo.GenePool(conf_obj)

# Initialize plotting variables
fitness = np.zeros((conf_obj.generations))

# Evolution loop
for i in range(conf_obj.generations):
    for j in range(pool.genomes):
        pool.fitness[j] = conf_obj.Fitness(pool.pool[j].T)
    fitness[i] = max(pool.fitness)  # Save fitness for plotting
    print('Highest fitness of generation ' + str(i) + ': ' + str(max(pool.fitness)))
    print('Best genome of generation ' + str(i) + ': ' + str(pool.pool[np.argmax(pool.fitness)]))
    pool.NextGen()

passed_test = np.linalg.norm(pool.pool[0] - 0) < 1E-12

plt.figure()
plt.plot(fitness)
plt.title(f'passed_test = {passed_test}')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
