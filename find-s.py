class Instance:
    def __init__(self, attributes, truth):
        if len(attributes) < 6:
            print("Not enough attributes")
            return
        self.attributes = attributes
        self.truth = truth
    
class Hypothesis:
    def __init__(self, constraints):
        if len(constraints) < 6:
            print("Not enough constraints")
            return
        self.constraints = constraints
    
    def __call__(self, x):
        for i in range(6):
            if self.constraints[i] == False: return False
            if self.constraints[i] == True:  continue
            
            if x.attributes[i] == self.constraints[i]: 
                continue
            else:
                #print(f"{x.attributes[i]} != {self.constraints[i]}")
                return False
        
        return True

class find_s:
    def __init__(self):
        self.s = Hypothesis([False]*6)

    def train(self, instance):
        if instance.truth == False: return
        for i in range(6):
            s_con  = self.s.constraints[i]
            x_attr = instance.attributes[i]

            if s_con == False:    self.s.constraints[i] = x_attr
            elif x_attr != s_con: self.s.constraints[i] = True

X = Instance
finds = find_s()
x1 = X(['sunny','warm','normal','strong','warm','same'], True)
x2 = X(['sunny','warm','high','strong','warm','same'],   True)
x3 = X(['rainy','cold','high','strong','warm','change'], False)
x4 = X(['sunny','warm','high','strong','cool','change'], True)

for i in [x1,x2,x3,x4]:
    finds.train(i)
    print(finds.s.constraints)

