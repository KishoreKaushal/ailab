import numpy as np 
import copy
import itertools

class Environment:
    def __init__ (self , wickets = 3 , overs = 10):
        self.wickets = wickets
        self.gamma = 1
        self.overs = overs
        self.bowlers = [(3, 33) , (3.5, 30) , (4, 24) , (4.5, 18) , (5, 15)]
        self.max_bowl_overs = 2
        self.overs_left = [self.max_bowl_overs for _ in range(len(self.bowlers))]
        
        self.action_set = list(range(len(self.bowlers)))

        self.V = dict()
        self.policy = dict()

        for element in itertools.product( [0,1,2] , [0,1,2] , [0,1,2], [0,1,2], [0,1,2], [0,1,2,3]):
            self.V[element] = 0
            self.policy[element] = 0


    def value_iteration(self , epsilon = 1e-4):

        cycles = 1000
        while True and cycles>=0:
            cycles-=1
            if cycles%50 == 0:
                print(cycles)

            delta = 0
            
            for s in self.V.keys():
                v = self.V[s]
                self.V[s] = -np.inf 

                for bowler in self.action_set:
                    temp = 0
                    s_next = list(s)
                    
                    if s_next[-1] == 0:
                        continue

                    if s_next[bowler] - 1 < 0:
                        continue

                    s_next[bowler] -= 1
                    
                    s_next = tuple(s_next)
                    # for out
                    temp += (6/self.bowlers[bowler][1]) * (self.bowlers[bowler][0])
                    temp += (1 - 6/self.bowlers[bowler][1]) * (self.bowlers[bowler][0] + self.gamma*self.V[s_next])

                    self.V[s] = max(self.V[s] , temp)
                
                if v > self.V[s]:
                    self.V[s] = v

                delta = max(delta , abs(v - self.V[s]))

                if delta <= epsilon:
                    break

            for s in self.policy.keys():
                b = self.policy[s]
                best_bowler = b

                temp = 0
                s_next = list(s)
                
                if s_next[-1] == 0:
                    continue

                if s_next[best_bowler] - 1 < 0:
                    continue

                s_next[best_bowler] -= 1
                s_next = tuple(s_next)
                # for out
                temp += (6/self.bowlers[best_bowler][1]) * (self.bowlers[best_bowler][0])
                temp += (1 - 6/self.bowlers[best_bowler][1]) * (self.bowlers[best_bowler][0] + self.gamma*self.V[s_next])
                
                for bowler in self.action_set:
                    ret = 0
                    s_next = list(s)
                
                    if s_next[-1] != 0 and s_next[bowler] - 1 >= 0:
                        s_next[bowler] -= 1    
                        # for out
                        s_next = tuple(s_next)
                        ret += (6/self.bowlers[bowler][1]) * (self.bowlers[bowler][0])
                        ret += (1 - 6/self.bowlers[bowler][1]) * (self.bowlers[bowler][0] + self.gamma*self.V[s_next])

                    if temp <= ret:
                        temp = ret
                        best_bowler = bowler

                self.policy[s] = best_bowler
        
        print("Optimal Strategy: ")
        start_state = [2,2,2,2,2,3]
        
        for bowler in 
        


def main():
    env = Environment()
    env.value_iteration()

if __name__ == "__main__":
    main()

