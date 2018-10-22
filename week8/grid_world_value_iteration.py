import numpy as np
import copy

# this function generates a random transition probability matrix
# sum of all the elements in each row is 1
def generate_transition_probability_matrix(k=4):
    result = np.identity(k) + np.random.uniform(low=0., high=.25, size=(k, k))
    result /= result.sum(axis=1, keepdims=1)
    return result

class Environment:
    # considering uniform policy i.e., probability of taking an action in a current state
    # actions are deterministic, i.e., resulting state of the agent on an action is deterministic
    def __init__(self, size , discount_factor ,step_reward = -100 , reward = 1000 , penalty = -5000 , p=0.13):
        self.size = size
        self.reward = reward
        self.step_reward = step_reward
        self.penalty = penalty
        self.outside_grid_penalty = -20
        self.action_set = {'up' , 'down' , 'left' , 'right'}
        self.discount_factor = discount_factor

        self.V = np.zeros((size,size))
        self.policy = [x[:] for x in [['up'] * self.size] * self.size]

        n = round(p * size * size)
        
        self.negative_states = set()
        self.reward_states = set()

        # generating 13% random negative states and 13% random reward states
        for _ in range(n):
            while True:
                neg = (np.random.randint(size) , np.random.randint(size))
                rew = (np.random.randint(size) , np.random.randint(size))
                temp_set = self.negative_states.union(self.reward_states)
                if (neg!=rew) and (neg not in temp_set) and (rew not in temp_set):
                    self.negative_states.add(neg)
                    self.reward_states.add(rew)
                    break
        

        print("Reward States Set: " , self.reward_states)
        print("Negative Reward States Set: " , self.negative_states)
        
        self.render()

    
    # ⛳ or $: Reward State
    # 🔥 or #: Negative State
    def render(self , grid=None):

        for i in range(self.size):
            for j in range(self.size):
                coord = (i,j)
                try:
                    if coord in self.reward_states:
                        print('⛳' ,end="\t")
                    elif coord in self.negative_states:
                        print('🔥' ,end="\t")
                    else:
                        print("-" ,end="\t")
                except:
                    if coord in self.reward_states:
                        print('$' ,end="\t")
                    elif coord in self.negative_states:
                        print('#' ,end="\t")
                    else:
                        print("-" ,end="\t")
            print("\n" , end="")

    @staticmethod
    def action_val(operator , state):
        return tuple({
            'up': lambda:  [-1,0],
            'down': lambda:  [1,0],
            'left': lambda:  [0,-1],
            'right': lambda: [0,1]
        }.get(operator , lambda: None)() + np.array(state))

    def transition_fuction_with_reward(self , state , action):
        new_state = Environment.action_val(action , state)

        # agent can't step outside the grid
        if (0 <= new_state[0] < self.size) and (0 <= new_state[1] < self.size):
            if (new_state in self.reward_states):
                # if new_state is reward state : then recieve heavy reward
                return tuple((new_state , self.reward))
            elif (new_state in self.negative_states):
                # if new_state is negative state : then receive heavy penalty
                return tuple((new_state , self.penalty))
            else:
                # in any other case agent will recieve a negative step reward
                return tuple((new_state , self.step_reward))
        else:
            # agent tried to go outside the grid, so it will get a negative penalty
            return tuple((state , self.outside_grid_penalty))

    def value_iteration(self, epsilon = 1e-4):
        policy = copy.deepcopy(self.policy) # uniform policy
        V = copy.deepcopy(self.V)
        size = self.size
        action_set = copy.deepcopy(self.action_set)
        gamma = self.discount_factor

        cycle = 0
        while True:
            cycle+=1
            delta = 0
            # for each state
            for i in range(size):
                for j in range(size):
                    s = (i,j)
                    v = V[s]
                    V[s] = -np.inf
                    # choose the maximum value
                    for action in action_set:
                        ret = self.transition_fuction_with_reward(s,action)
                        V[s] = max(V[s] , (ret[1] + gamma * V[ret[0]]))
                    
                    delta = max(delta , abs(v - V[s]))
            
            if delta <= epsilon:
                break

        # find a deterministic policy for all states
        for i in range(size):
            for j in range(size):
                s = (i,j)
                
                b = policy[i][j]
                action_best = b
                ret = self.transition_fuction_with_reward(s,action_best)
                temp = (ret[1] + gamma * V[ret[0]])

                for action in action_set:
                    ret = self.transition_fuction_with_reward(s,action)
                    if temp <= (ret[1] + gamma * V[ret[0]]):
                        temp = (ret[1] + gamma * V[ret[0]])
                        action_best = action

                policy[i][j] = action_best

        print("Total Iterations: " , cycle)
        print(V , "\n\n")
        for i in range(len(policy)):
            print(policy[i])


def main():
    size = np.random.randint(2 , 7)
    env = Environment(size , 0.75)
    env.value_iteration()

if __name__ == "__main__":
    main()
