#class Perceptron:

import numpy  as np
import random as r

'''
struct:
O
 \
  O
 /
O
'''



class Perc:
    def __init__(self, weights = [.5]*3):
        self.w = weights
        self.m = []
        
    def examples(number):
        examples = []
        for i in range(number):
            xs = [1,  r.randint(-100,100), r.randint(-100,100)]
            examples.append([xs, Perc.target(xs)])
        return examples

    def target(xs): return 1 if xs[1] + 2*xs[2] > 2 else 0

    def error(self, xs): return .5*(Perc.target(xs) - self.lf(xs))**2

    def lf(self,xs):
        val = 0
        for w,x in zip(self.w,xs):
            val += w*x
        return 1 if val > 0 else 0

    def l(self,x1,x2):
        return bool(self.lf([1,x1,x2]))

    def train(self,examples):
        for xs,t in examples:
            for i in range(3):
                self.w[i] += .1*( t - self.lf(xs) )*(xs[i])
            

    def main(self):
        self.train(Perc.examples(1000000))

p = Perc()#[-103.3999999999984, 129.19999999999956, 258.20000000000107])
p.main()

'''
[-1.9000000000000001, 36.39116143722741, 33.876743526105386]
[-0.5000000000000002, 17.972292472243918, 21.530930939972272]
[-2.1, 18.15980465690697, 20.63326105787856]
[-0.5000000000000002, 6.215274629297628, 17.630918121671215]

USE THIS:
[-34.100000000000215, 16.80000000000009, 33.60000000000004]
'''
