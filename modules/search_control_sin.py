#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 12:37:08 2018

@author: ljknoll
more than one network in serie with NLLLoss, 
where the logprobabilities are obtained by single_value_probabilities in results folder.

Single Input Network (sin)
"""

import torch
import numpy as np
from Nets.predNNet import predNNet
from Nets.webNNet import webNNet
import matplotlib.pyplot as plt
import pickle

# data import
data_dir = r'/home/lennart/Desktop/2018_11_02_142235_CP_inputs_and_targets.npz'
data = np.load(data_dir)
input_data = torch.tensor(data['inputs']).float()
target_data = torch.tensor(data['target']).long()+1

# network import
main_dir = r'/home/lennart/Desktop/nnweb/'
data_dir = 'lr2e-4_eps400_mb512_20180807CP.pt'
net1 = predNNet(main_dir+data_dir)

web = webNNet()
web.add_vertex(net1, 'A', output=True)
web.add_vertex(net1, 'B')
#web.add_vertex(net1, 'C')
#web.add_vertex(net1, 'D')
#web.add_vertex(net1, 'E')

web.add_arc('B', 'A', 3)
#web.add_arc('C', 'B', 6)
#web.add_arc('D', 'C', 5)
#web.add_arc('E', 'D', 6)

batch_size = 300
nr_epochs = 100
lr = 0.01
beta = 0.1
cv_reset = 'rand' # 0.6*torch.ones(5) # None, 'rand', tensor(5)
bias = True
scale = True

optimizer = torch.optim.Adam
betas=(0.9, 0.99)
eps=1e-08

weights = torch.bincount(target_data[:,0]).float()
weights = 1/weights
weights /= torch.sum(weights)

# thresholds between p0 & p1 and p1 & p2
d0 = -0.5
d2 = 0.5
exp_factor = 10

delta = d2-d0
w = exp_factor/delta

custom_loss = torch.nn.NLLLoss(weight = weights)
def loss_fn(y_pred, y):
    d1 = w*(-d0-d2)
    wy_pred = w*y_pred
    
    # calculate log probabilities
    p0 = -torch.log(1 + torch.exp(wy_pred-d0*w) + torch.exp(2*wy_pred+d1))
    p1 = -torch.log(torch.exp(-wy_pred+d0*w) + 1 + torch.exp(wy_pred-d2*w))
    p2 = -torch.log(torch.exp(-2*wy_pred-d1) + torch.exp(-wy_pred+d2*w) + 1)
    return custom_loss(torch.cat((p0, p1, p2), 1), y[:,0])


#I0 = [-0.9, 0., 0.9]
#I1 = [-0.9, -0.6, -0.3, 0., 0.3, 0.6, 0.9]
I0 = [0.0]
I1 = [-0.3]
inputs_list = []
for i0 in I0:
    for i1 in I1:
        inputs_list.append((i0,i1))

results = {}
for inp in inputs_list:
    cat_input_data = torch.cat((torch.tensor(inp).repeat(input_data.shape[0], 1), input_data), 1)
    print(inp)
    web.reset_parameters(cv_reset)
    loss, best_cv = web.train(cat_input_data, target_data, 
                         beta=beta,
                         batch_size=batch_size,
                         nr_epochs=nr_epochs,
                         optimizer=optimizer,
                         loss_fn=loss_fn,
                         lr = lr,
                         betas = betas,
                         eps = eps,
                         bias = bias,
                         scale = scale)
    results[inp] = {'input':cat_input_data, 'loss':loss, 'best_cv':best_cv}


def plot_results(best_cv, conf, input_data):
    web.reset_parameters(best_cv)
    s = best_cv['scale']
    b = best_cv['bias']
    s_r = list(map(lambda x: round(x,1), s.tolist()))
    b_r = list(map(lambda x: round(x,1), b.tolist()))
    web.forward(input_data, verbose=True)
    output_data = web.get_output()
    classifications = (output_data>d0)[:,0] + (output_data>d2)[:,0]
    plt.figure()
    plt.plot(target_data.float()+0.01)
    plt.plot(output_data)
    plt.plot(classifications)
    class_error = torch.sum(abs(target_data.float()[:,0]-classifications.float()))/150/21
    print('classification error: %s, loss: %s' % (class_error.item(), min(loss)))
#    plt.plot(input_data.sum(1)) # summed current of input
    plt.legend(['target', 'scaled output', 'classification'])
    plt.title('%s, output_data vs target data, scale:%s, bias:%s' % (conf, s_r, b_r))
    plt.show()


for key,value in results.items():
#key = (-0.9, -0.9)
#value = results[key]
    print(key)
    print('loss: %s' % min(value['loss']))
    plot_results(value['best_cv'], key, value['input'])
#    break


#plt.figure()
#plt.plot(loss)
#plt.show()

if False:
    with open('dict.pickle', 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
if False:
    with open('dict.pickle', 'rb') as handle:
        b = pickle.load(handle)
