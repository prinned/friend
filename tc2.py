#!/usr/bin/env python3
from copy import deepcopy, copy
import random
import numpy as np

class Game:
    def __init__(self):
        self.bs = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
        self.turn = 0
        self.end = None
        self.trace = []


class Network:
    def __init__(self, ni, nh, no, lc = 0.3):
        self.weights = [np.random.rand(nh, ni) , 
                        np.random.rand(no, nh) ]
        
        self.biases  = [np.random.rand(nh) - 0, np.random.rand(no) - 0]
        
        self.nodes   = [np.zeros(nh), np.zeros(no)]
        self.lc = lc

    def act(array):
        return np.where(array > 0, array, array * 0.0001)
        #return np.where(array > 0, array, 0)
    
    def act_prime(array):
        return np.where(array > 0, 1, 0.0001)
        #return array > 0


    def forward(self, inputNodes):
        z_h = np.dot(self.weights[0], inputNodes) + self.biases[0][:,np.newaxis]
        self.nodes[0] = Network.act(z_h)
        z_o = np.dot(self.weights[1], self.nodes[0]) + self.biases[1][:,np.newaxis]
        self.nodes[1] = Network.act(z_o)
        return self.nodes[1]

    def backprop(self, inputs, target_outputs):
        self.forward(inputs)

        output_error = Network.act_prime(self.nodes[1]) * (target_outputs - self.nodes[1])
        #print(output_error.shape)
        hidden_error = np.dot(self.weights[1].transpose(), output_error) * Network.act_prime(self.nodes[0])
        
        #print("error\n\n\n", output_error, "")
        #print("", hidden_error, "\n\n\n")
        #print(hidden_error.shape)
        self.biases[0] += self.lc * np.sum(hidden_error, axis=1) / len(examples[0])
        self.biases[1] += self.lc * np.sum(output_error, axis=1) / len(examples[0])

        ##print(self.weights[0], "\n\n", self.lc * np.dot(hidden_error, inputs.transpose()))
        self.weights[0] += self.lc * np.dot(hidden_error, inputs.transpose()) / len(examples[0])
        #print(self.weights[0].shape, np.dot(hidden_error, inputs.transpose()).shape)
        self.weights[1] += self.lc * np.dot(output_error, self.nodes[0].transpose()) / len(examples[0])
        ##print(self.weights[0],"\n\n\n\n")
        ##print(self.weights[0] - self.lc * np.dot(hidden_error, inputs.transpose()))


check = Network(2,1,2)
#print("weights: ", check.weights)
#print("\n\n\n\n")


examples = np.array([
    np.random.rand(100),    
    np.random.rand(100),
])

target = np.array([
    [34]*100,
    [50]*100,
])
for i in range(1000):
    check.backprop(examples, target)
    print("",check.forward(np.array([
    [.5],[.5]
])).transpose(),"")



print(check.weights[0])
print(check.weights[1])
print(check.biases[0])
print(check.biases[1])
print()



##print("biases: \n",check.backprop(examples, examples)[1][0])
#check.backprop(examples, target)