#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:46:45 2018
This script is an example on how to construct and train a web of multiple neural networks to achieve a task.
@author: ljknoll
"""
import torch
from Nets.predNNet import predNNet
from Nets.webNNet import webNNet


# create nn object from which the web is made
main_dir = r'/home/lennart/Desktop/nnweb/'
data_dir = 'lr2e-4_eps400_mb512_20180807CP.pt'
net1 = predNNet(main_dir+data_dir)


# Initialize web object
web = webNNet()

# add networks as vertices
# network object, name of vertex
web.add_vertex(net1, 'A', output=True)
web.add_vertex(net1, 'B')

# connect vertices with arcs, source->sink
# source vertex, sink vertex, sink gate index
web.add_arc('B', 'A', 2)

# Check if web is valid (and optionally plot)
#web.check_graph(print_graph=True)

N = 10  # batch_size

# different train data:
#train_data = torch.zeros(N, 4)
#train_data[:,1] = 0.2
#train_data[:,3] = 0.3

# repeat train data for all vertices:
train_data = torch.zeros(N,2)
train_data[:,1] = 0.9

# target data 
targets = 0.5*torch.ones(N,1)

loss = web.train(train_data, targets, beta=0.01)