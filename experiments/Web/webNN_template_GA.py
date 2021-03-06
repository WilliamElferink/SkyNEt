#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:07:01 2018

@author: ljknoll

Testing evolution script for training web of neural networks, both GA and GD

"""
import torch
import matplotlib.pyplot as plt

from SkyNEt.modules.Nets.staNNet import staNNet
from SkyNEt.modules.Nets.webNNet import webNNet
import SkyNEt.experiments.boolean_logic.config_evolve_NN as config

# Iinitialize GA config object
cf = config.experiment_config()
cf.generations = 50
cf.mutationrate = 0.1
cf.fitnessavg = 1

# Initialize NN
nn_file = r'/home/lennart/Dropbox/afstuderen/search_scripts/lr2e-4_eps400_mb512_20180807CP.pt'
net = staNNet(nn_file)

# build web
web = webNNet()
web.add_vertex(net, 'A', output=True)


# batch size
N = 7
# input data, size (N, 2 * nr of networks)
x = torch.cat((torch.zeros(N), torch.linspace(-0.9, 0.9, N))).view(2, -1).t()
# target data, size (N, nr output vertices)
target = torch.linspace(0, 0.5, N).view(-1,1)


geneArray, outputArray, fitnessArray = web.trainGA(x, target, cf, verbose = True)

# plot error vs generations
plt.figure()
plt.plot(-fitnessArray[:,0])
plt.title('GA error')

# plot best output
plt.figure()
plt.plot(outputArray[-1, 0])
plt.plot(target.numpy())
plt.legend(['web output', 'target'])
plt.title('GA output')


web.reset_parameters()
loss, params, param_history = web.train(x, target, batch_size=1, max_epochs=200, lr=0.05, beta=0.1, verbose=True)

web.reset_parameters(params)
web.forward(x)

plt.figure()
plt.plot(loss)
plt.title('GD error')

plt.figure()
plt.plot(web.get_output().view(-1,1).numpy())
plt.plot(target.numpy())
plt.legend(['web output', 'target'])
plt.title('GD output')


print('GA cv: %s' % geneArray[-1,0])
print('GD cv: %s' % params['A'])