import math
import numpy as np
import random

def sigmoid(l): return [1/(1+math.exp(-i)) for i in l]

class Network:
    def __init__(self,ni,nh,no, lc = 0.3):
        self.w = np.array([np.random.rand(nh,ni), np.random.rand(no,nh)])
        self.a = np.array([np.zeros(ni), np.zeros(nh), np.zeros(no)])
        self.b = np.array([np.random.rand(nh), np.random.rand(no)])
        self.ni = ni
        self.nh = nh
        self.no = no
        self.lc = lc #learning constant

    def ff(self, xs):
        self.a[0] = xs
        for layer in [0,1]:
            z = np.dot(self.w[layer], self.a[layer]) + self.b[layer]
            self.a[layer+1] = sigmoid(z)

    def back(self, epochs, examples):
        for q in range(epochs):
            for xs,t in examples:
                self.ff(xs)

                del_k = np.zeros(self.no)
                for o in range(self.no):
                    u = self.a[-1][o]
                    del_k[o] = u * (1 - u) * (t[o] - u)

                    for h in range(self.nh):
                        self.w[1][o][h] += self.lc * del_k[o] * self.a[1][h]

                    self.b[1][o] += self.lc * del_k[o]

                for h in range(self.nh):
                    Sum = 0
                    for o in range(self.no):
                        Sum += self.w[1][o][h]*del_k[o]

                    u = self.a[1][h]
                    del_h = u * (1 - u) * Sum

                    for i in range(self.ni):
                        self.w[0][h][i] += self.lc * del_h * self.a[0][i]

                    self.b[0][h] += self.lc * del_h

    def r(self,l=-1): print([round(i) for i in x.a[l]])
    def nr(self,l=-1): print([(i) for i in x.a[l]])
                    

x = Network(32,5,32)

examples = []
for i in range(32):
    a = [0]*32
    a[i] = 1
    examples.append([a,a])

x.back(6000, examples) #for a (16,4,16) network, you only need 3000 epochs

for i,j in examples:
    x.ff(i)
    x.r()
    x.r(1)
    print()
