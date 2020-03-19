#!/usr/bin/env python3
import act_functions
import numpy as np

class Network:
    def __init__(self, node_nums, act_funcs, lc = 0.3):
        #first act_func is ignored!
        self.num_of_layers = len(node_nums)
        self.node_nums = node_nums
        
        assert(self.num_of_layers == len(act_funcs))
        
        self.act_funcs = [act_functions.act_dir[i] for i in act_funcs]
        self.weights   = [np.random.rand(node_nums[i], node_nums[i - 1]) - 0.5 for i in range(1, self.num_of_layers)]
        self.biases    = [np.random.rand(i) - 0.5 for i in node_nums[1::]]
        self.nodes     = [0]*(self.num_of_layers)
        
        self.lc = lc

    def forward(self, inputNodes):
        self.nodes[0] = inputNodes
        for i in range(self.num_of_layers - 1):
            z = np.dot(self.weights[i], self.nodes[i]) + self.biases[i][:,np.newaxis]
            self.nodes[i + 1] = self.act_funcs[i][0](z)
        return self.nodes[-1]

    #forward only one 
    def forward1(self, inputNodes):
        self.nodes[0] = inputNodes
        for i in range(self.num_of_layers - 1):
            z = np.dot(self.weights[i], self.nodes[i]) + self.biases[i]
            self.nodes[i + 1] = self.act_funcs[i][0](z)
        
        return self.nodes[-1]

    def backprop(self, inputs, target_outputs):
        num_of_examples = inputs.shape[1]
        self.forward(inputs)
        error = self.act_funcs[-1][1](self.nodes[-1]) * (target_outputs - self.nodes[-1])
        
        self.weights[-1] += self.lc * np.dot(error, self.nodes[-2].T)   / num_of_examples
        self.biases[-1]  += self.lc * np.sum(error, axis=1)             / num_of_examples
        
        previous_error = error
        for i in range(self.num_of_layers - 2, 0, -1):
            error = np.dot(self.weights[i].T, previous_error) * self.act_funcs[i][1](self.nodes[i])
            self.biases[i - 1]  += self.lc * np.sum(error, axis=1)            / num_of_examples
            self.weights[i - 1] += self.lc * np.dot(error, self.nodes[i-1].T) / num_of_examples
            previous_error = error

class AE_tied(Network):
    def __init__(self, node_spec, act_spec, lc = 0.3):
        self.encoder = Network(node_spec, act_spec, lc)
        self.decoder = Network(node_spec[::-1], act_spec)

'''
n = 8
check = Network([n, 3, n], [None, "relu6", "relu"])
e = np.identity(n)
#while(True):
for i in range(1000000):
    check.backprop(e, e)
    r = check.forward(e)
    if (np.argmax(e, axis = 1) == np.argmax(r, axis = 1)).all(): break
print(i)
print(np.argmax(e, axis = 1))
print(np.argmax(r, axis = 1))
'''