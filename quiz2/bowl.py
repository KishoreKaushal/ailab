import numpy as np
import copy

class Environment:
    def __init__(self):
        self.gamma = 1.0
        self.wickets = 3
        self.overs = 10
        self.economy = [3, 3.5, 4, 4.5, 5]
        self.strike = [33, 30, 24, 18, 15]

        self.V = np.zeros((self.overs + 1, self.wickets + 1, (1 << 10)))
        self.policy = np.zeros((self.overs + 1, self.wickets + 1, (1 << 10)), dtype = np.int)

    def calculate_optimal_strategy(self , overs, wickets, mask):
        if overs == 0 or wickets == 3:
            return 0

        if self.V[overs, wickets, mask]!=0:
            return self.V[overs,wickets,mask]

        index = -1
        smin = np.inf

        for i in range(0,10):
            new_mask = mask ^ (1<<i)
            if mask & (1<<i) != 0:
                p = 6 / self.strike[i//2]
                v = self.economy[i // 2] + self.gamma * (p * self.calculate_optimal_strategy(overs - 1, wickets + 1, new_mask) + (1 - p) * self.calculate_optimal_strategy(overs - 1, wickets, new_mask))
                if v < smin:
                    smin = v
                    index = i
        
        self.V[overs, wickets, mask] = smin
        self.policy[overs,wickets,mask] = index
        return smin

    def get_optimal_strategy(self):
        val = self.calculate_optimal_strategy(10 , 0 , int((1<<10)-1))
        print("Expected Value after calculation: {}".format(val))

    def simulate(self):
        value = 0
        wickets = 0
        mask = (1<<10) - 1

        for i in range(10,0,-1):
            if wickets == 3:
                break
            bowler = self.policy[i][wickets][mask]
            prob = np.random.random()
            wickets += (prob < (6/self.strike[bowler//2]))
            mask = mask ^ (1 << bowler)
            value += self.economy[bowler // 2]
            print (i, wickets, bin(mask)[2:], bowler // 2)
        return value

def main():
    env = Environment()
    env.get_optimal_strategy()
    
    # perform simulations
    number_of_simulations = 5
    total_val = 0
    for i in range(number_of_simulations):
        print("\n--------------------------------------------------\n")
        val = env.simulate()
        total_val += val
    
    print("\n--------------------------------------\nAverage Val: {}".format(total_val/number_of_simulations))


if __name__=="__main__":
    main()
        