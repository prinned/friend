#!/usr/bin/env python3
import numpy as np

#-----hyperparameters------
leaky_relu_slope = 0.001
relu6_maximum    = 6
#--------------------------

def relu(array):      return np.where(array > 0, array, 0)
def d_relu(array):    return array > 0

def lrelu(array):     return np.where(array > 0, array, leaky_relu_slope*array)
def d_lrelu(array):   return np.where(array > 0, 1, leaky_relu_slope)

def relu6(array):     return array.clip(0, relu6_maximum)
def d_relu6(array):   return np.where( (array > 0) & (array < relu6_maximum), 1, 0)

def tanh(array):      return np.tanh(array)
def d_tanh(array):    return 1 - array**2

def sigmoid(array):   return 1 / (1 + np.exp(-array))
def d_sigmoid(array): return array*(1 - array)

def linear(array):    return array
def d_linear(array):  return np.ones_like(array)

def softmax(array):
    e_arr = np.exp(array)
    return e_arr / np.sum(e_arr.T, axis = 1)

act_dir = {
    None         : (linear   , d_linear   ),
    "linear"     : (linear   , d_linear   ),
    "relu"       : (relu     , d_relu     ),
    "lrelu"      : (lrelu    , d_lrelu    ),
    "relu6"      : (relu6    , d_relu6    ),
    "tanh"       : (tanh     , d_tanh     ),
    "sigmoid"    : (sigmoid  , d_sigmoid  ),
}

#print(act_dir["relu6"][0](np.array([-100, 23, 3, 34, -34])))
'''
a = np.array([[24,34,44,54],
              [24,34,100,54],
              [24,34,44,54],
              [24,34,44,54]])

e_arr = np.exp(a)
print(e_arr)
print(np.sum(e_arr.T, axis = 1))
print(softmax(a))
'''