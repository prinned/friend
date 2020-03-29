#!/usr/bin/env python3

sensors = [1,2,3]
outs    = [4,5]
hidden  = []
node_num = 8


con1    = [1,3,2,7,6,7,8,6]
con2    = [6,7,7,6,8,8,5,4]
weights = [1,1,1,1,1,1,1,1]


class Genome:
    all_innov = []
    sensor_num = 3
    output_num = 2

    def __init__(self, innov_list, weights, disable_mask, total_nodes):
        self.innov_list = innov_list
        self.weights = weights
        self.disable_mask = disable_mask
        self.total_nodes = total_nodes
        self.act_func = lambda x : x/2
    
    def forward(self, input_vals):
        act_mask     = [1]*(1 +  Genome.sensor_num) + [0] * (self.total_nodes - Genome.sensor_num)
        nodes = [1] + [0]*(self.total_nodes)
        nodes[1:(Genome.sensor_num+1)] = input_vals
        print(nodes)
        print(act_mask)
        print(self.innov_list)
        for i in self.innov_list: 
            print(Genome.all_innov[i])
            if act_mask[Genome.all_innov[i][0]] == False: 
                nodes[Genome.all_innov[i][0]] = self.act_func(nodes[Genome.all_innov[i][0]])
            nodes[Genome.all_innov[i][1]] += self.weights[i]*nodes[Genome.all_innov[i][0]]
        return nodes[(self.total_nodes - Genome.output_num + 1):]

Genome.all_innov = list(zip(con1,con2))
g = Genome(list(range(8)), weights, [0]*8, 8)
print(g.forward([0,0,0]))