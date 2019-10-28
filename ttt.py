from copy import deepcopy, copy
import random

class Game:
    def __init__(self):
        self.bs = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
        self.turn = -1
        self.end = None
        self.trace = []

    @staticmethod
    def draw(bs):
        for i in [0,1,2]:
            print(i,'|',sep='',end='')
            for j in [0,1,2]:
                if bs[i][j] == -1:  text = 'O'
                elif bs[i][j] == 0: text = ' '
                elif bs[i][j] == 1: text = 'X'

                print(text,'|',sep='',end='')
            print()
        print("  0 1 2 \n")
                
        print()
        
    def inverted(self):
        return [[i*-1 for i in j] for j in self.bs]

    def play(self, y,x):
        if self.end != None:
            print("BOARD ALREADEY ENDED")
            return

        if self.bs[y][x] != 0:
            print("MOVE ALREADY PLAYED")
            return

        if self.turn % 2 == 1: sign =  1
        else:                  sign = -1

        self.bs[y][x] = sign
        self.trace.append(deepcopy(self.bs))
        self.turn+=1

        if Game.checkwin(self.bs, sign) == True:
            self.end = sign

        draw = True
        for i in [0,1,2]:
            for j in [0,1,2]:
                if self.bs[i][j] == 0: draw = False
        if draw:
            self.end = 0

    @staticmethod
    def diagnols(board):
        d1 = [board[0][0], board[1][1], board[2][2]]
        d2 = [board[0][2], board[1][1], board[2][0]]
        return [d1,d2]

    @staticmethod
    def rows(board):
        return [[board[i][j] for j in [0,1,2]] for i in [0,1,2]]

    @staticmethod
    def cols(board):
        return [[board[j][i] for j in [0,1,2]] for i in [0,1,2]]

    @staticmethod
    def checkwin(board, sign):
        for j in [Game.rows(board), Game.cols(board), Game.diagnols(board)]:
            for i in j:
                if sum(i) == 3*sign: return True
        return False
        
class AI:
    def __init__(self, weights = [.5]*7):
        self.weights = weights
    #-------------- making val and move----------------------
    @staticmethod
    def xs(board, sign):
        xs = [1,0,0,0,0,0,0] #x0 is 1 so it wont affect the constant weight
        '''
        x0 = always 1 so it doesnt affect w0 (just to make func simpler)
        x1 = X win
        x2 = O win
        x3 = 2 X's in a line and open square
        x4 = 2 O's in a line and open square
        x5 = 1 X in empty line
        x6 = 1 O in empty line
        '''
        for j in [Game.rows(board), Game.cols(board), Game.diagnols(board)]:
            for i in j:
                if sum(i) ==  3*sign: xs[1] += 1
                if sum(i) == -3*sign: xs[2] += 1
                if sum(i) ==  2*sign: xs[3] += 1
                if sum(i) == -2*sign: xs[4] += 1
                
                if(sum(i) ==  sign
                and 0 in i):          xs[5] += 1
                
                if(sum(i) == -sign
                and 0 in i):          xs[6] += 1
        return xs
    
    def value(self, board, sign): 
        val = 0
        for (weight,x) in zip(self.weights, AI.xs(board, sign)):
            val += weight*x
        return val

    def value_xs(self, xs): 
        val = 0
        for (weight,x) in zip(self.weights, xs):
            val += weight*x
        return val 

    def move(self, board, sign):
        spaces = []
        for y in [0,1,2]:
            for x in [0,1,2]:
                if board[y][x] == 0: spaces.append([y,x])
        
        val_list = []
        for (y,x) in spaces:
            bcopy = deepcopy(board)
            bcopy[y][x] = sign
            val_list.append([ [y,x] , self.value(bcopy, sign) ])

        best_val   = 0
        best_space = spaces[0]
        for val in val_list:
            if val[1] > best_val: 
                best_space = val[0]
                best_val   = val[1]

        return best_space
    
    #-------------- making the rest----------------------   
    def perf_system(self):
        g = Game()

        while g.end == None:
            move = self.move(g.bs, 1)
            g.play(move[0], move[1])
            if g.end != None: break

            move = self.move(g.bs, -1)
            g.play(move[0], move[1])
        return g.trace

    def critic(self, trace):        
        examples = []

        for i in range(len(trace)):
            if i == len(trace) - 2: continue
            
            bs = trace[i]
            xs = AI.xs(trace[i], 1)
            if i == len(trace) - 1:
                if AI.xs(bs, 1)[1] > 0:
                    examples.append([xs, 100])

                
                elif AI.xs(bs, 1)[2] > 0:
                    examples.append([xs, -100])

                else:
                    examples.append([xs,0])
                    
            else:
                xs_successor = AI.xs(trace[i+2], 1)
                examples.append([xs, self.value_xs(xs_successor)])
        return examples
    
    def generalizer(self,examples):
        turn = 0
        for [xs, v_train] in examples:
            value = self.value_xs(xs)
            for i in range(7):
                self.weights[i] +=  0.1 * (v_train - value) * xs[i]
            turn+=1
                

    def learn(self,times):
        for i in range(times):
            self.generalizer(self.critic(self.perf_system()))
        for i in range(7):
            print('Weight', i, '-', self.weights[i])
        print(self.weights)
#------------------------------- THE PROGRAM ENDED THE REST DOESNT COUNT----------------

#use this to play with computer, technically program ended        
def cp(times, compfirst):
    #there's little difference beyond 1000
    if times < 1000 or times > 5000:
        test_dummy = AI([0.5]*7)
        test_dummy.learn(times)
        weights = test_dummy.weights
    elif times == 1000:
        weights = [-3.2264838459777887, 43.18300301725494, -85.52920153592079, 15.988065375567771, -13.19102458628005, 10.84259560908655, -10.979917281961045]
    elif times == 5000:
        weights = [-3.224194903566711, 42.70469876546411, -84.98978105070327, 17.7741356970466, -15.459463405606419, 8.675499829889187, -8.463629301028567]
    elif times == -5000:
        weights = [1.3410638946117552, -92.37846313528837, -8.648843426955215, -1.0362706074550727, 0.04611568975271118, 0.3216494217844299, -6.832248037914471]
    g = Game()
    ai2 = AI(weights)

    Game.draw(g.bs)
    if compfirst:
        while g.end == None:
            g.play(ai2.move(g.bs,1)[0],ai2.move(g.bs,1)[1])
            g.draw(g.bs)
            if g.end != None: break

            x = int(input("X: "))
            y = int(input("Y: "))
            g.play(y, x)
            Game.draw(g.bs)
    else:
        while g.end == None:
            x = int(input("X: "))
            y = int(input("Y: "))
            g.play(y, x)
            Game.draw(g.bs)
            if g.end != None: break

            
            g.play(ai2.move(g.bs,1)[0],ai2.move(g.bs,1)[1])
            g.draw(g.bs)

if __name__ == "__main__":
    cp(5000, False)
