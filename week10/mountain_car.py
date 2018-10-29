import numpy as np
import copy
import matplotlib.pyplot as plt

class Environment:
    # considering uniform policy i.e., probability of taking an action in a current state
    # actions are deterministic, i.e., resulting state of the agent on an action is deterministic
    def __init__(self , discount_factor = 1):
        self.discount_factor = discount_factor
        self.velocity = (-0.07 , 0.07)
        self.position = (-1.2 , 0.6)
        self.gridsize = 100
        self.goal_reached_reward = 1
        self.goal_not_reached_reward = -1
        self.velocity_grid = np.linspace(self.velocity[0] , self.velocity[1] , self.gridsize)
        self.position_grid = np.linspace(self.position[0], self.position[1] , self.gridsize)
        self.position_step = self.position_grid[1] - self.position_grid[0]
        self.velocity_step = self.velocity_grid[1] - self.velocity_grid[0]
        self.grid = []
        
        self.V = np.zeros((self.gridsize,self.gridsize))
        self.policy = np.zeros((self.gridsize,self.gridsize))

        for velocity in self.velocity_grid:
            self.grid.append([(velocity , position) for position in self.position_grid])

        self.action_set = [-1, 0, 1]
        pass

    def update_function(self , current_pos , current_vel , action):
        next_vel = current_vel + (action * 0.001) + np.cos(3 * current_pos)*(-0.0025)
        next_vel = min(max(next_vel , self.velocity[0]) , self.velocity[1])

        next_pos = current_pos + next_vel*1     # because time step is always 1
        next_pos = min(max(next_pos , self.position[0]) , self.position[1])

        if (next_pos <= self.position[0]):
            next_vel = 0
        
        return (next_pos , next_vel)

    def get_posidx_velidx(self , pos , vel):
        posidx = int(np.ceil((pos - self.position_grid[0])/self.position_step))
        velidx = int(np.ceil((vel - self.velocity_grid[0])/self.velocity_step))
        
        if posidx >= self.gridsize:
            posidx = self.gridsize - 1
        
        if velidx >= self.gridsize:
            velidx = self.gridsize - 1
            
        return (posidx , velidx)

    def is_goal_reached(self , pos):
        return (pos >= self.position_grid[-1])

    def get_state(self, posidx , velidx):
        return (self.position_grid[posidx] , self.velocity_grid[velidx])


    def transition_fuction_with_reward(self , state_idx , action):
        current_vel , current_pos = self.grid[state_idx[0]][state_idx[1]]
        next_pos , next_vel = self.update_function(current_pos , current_vel , action)
        next_posidx , next_velidx = self.get_posidx_velidx(next_pos , next_vel)
        
        if (self.is_goal_reached(next_pos)):
            return tuple((tuple((next_velidx , next_posidx)) , self.goal_reached_reward))
        return tuple((tuple((next_velidx , next_posidx)) , self.goal_not_reached_reward))

    def value_iteration(self, epsilon = 1e-4):
        gamma = self.discount_factor
        policy = copy.deepcopy(self.policy)
        V = copy.deepcopy(self.V)
        action_set = copy.deepcopy(self.action_set)
        gridsize = self.gridsize

        # start the value iteration
        time_step = 0
        cycles = 1000
        while True and cycles >= 0:
            time_step+=1
            cycles -= 1
            delta = 0
            if (time_step%10 == 0):
                print("Time Step: {}".format(time_step))
            
            # for all state
            for velidx in range(gridsize):
                for posidx in range(gridsize):
                    state_idx = (velidx , posidx)
                    v = V[state_idx]
                    V[state_idx] = - 100000
                    
                    for action in action_set:
                        ret = self.transition_fuction_with_reward(state_idx,action)
                        V[state_idx] = max(V[state_idx] , (ret[1] + gamma * V[ret[0]]))
                            # print(state_idx , ret)
                            # return
                    delta = max(delta , abs(v - V[state_idx]))

            if (delta <= epsilon):
                break


        # find a deterministic policy for all states
        for velidx in range(gridsize):
            for posidx in range(gridsize):
                state_idx = (velidx , posidx)
                b = policy[state_idx]
                action_best = b

                ret = self.transition_fuction_with_reward(state_idx,action_best)
                temp = (ret[1] + gamma * V[ret[0]])

                for action in action_set:
                    ret = self.transition_fuction_with_reward(state_idx,action)
                    if temp <= (ret[1] + gamma * V[ret[0]]):
                        temp = (ret[1] + gamma * V[ret[0]])
                        action_best = action

                policy[state_idx] = action_best

        print("Total Iterations: " , cycles)
        print(V , "\n\n")
        print(policy , "\n\n")
        
        np.savetxt("value.txt", V, fmt = "%i")
        np.savetxt("policy.txt", policy, fmt = "%i")

        plt.imshow(V, cmap = "hot" , interpolation="nearest")
        plt.show()


def main():
    env = Environment()
    env.value_iteration()

if __name__ == "__main__":
    main()
