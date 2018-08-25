#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Week 3
# Other Group Members: Saptdeep Das (111601020) , Pankaj Kumar (111601014)
# Question No. 1

# Usage : curse_of_dimensionality.py  d L
# where d and L are the areguments to the program representing dimension and length

# This program is a generalized to cover all the cases of (d,L).
# Hence all the three environments(1D , 2D, 3D) can be simulated by passing the argument value accodingly.

import sys 
import numpy as np
from time import time

class Environment:
    '''
        This is generalized program for creating the environment with same principle.

        _d : dimension of the environment
        _L : is the length of a particular axis

        agent_position : List containing the current position of the agent.
        actions : stores all possible actions that the agent can take
        total_actions : total number of possible actions
    '''
    def __init__(self , _d , _L ):
        self.d = int(_d)
        self.L = int(_L)
        self.agent_position = (int(np.ceil(self.L/2))* np.ones(self.d).astype(np.int))
        
        self.actions = np.vstack((np.eye(self.d) , -np.eye(self.d))).astype(int)
    
        self.total_actions = int(2*self.d)
        
        print("Environment Initialized With: ")
        print("Dimension : {0}".format(self.d))
        print("L : {0}".format(self.L))
        print("Total Actions : {0}".format(self.total_actions))
        print("Agent Position : {0}".format(self.agent_position))
        print("Actions: \n{0}".format(self.actions))
    
    def get_total_actions_count(self):
        return self.total_actions

    def get_actions(self):
        return self.actions

    def interact(self , action_idx):
        # current_action = np.array(self.actions[action_idx] , np.int)
        current_action = self.actions[action_idx]

        agent_current_position = self.agent_position

        # print("This should be new: " , current_action + self.agent_position)
        self.agent_position = current_action + self.agent_position
        # print("This is the new: " , self.agent_position)
        # print(np.where(self.agent_position > self.L))

        # if some of the coordinates is greater than L
        if np.where(self.agent_position > self.L)[0].shape[0] != 0 or \
        np.where(self.agent_position < 0)[0].shape[0] != 0:
            self.agent_position = agent_current_position
            # print("But why changed back to: " , self.agent_position)

    def feedback(self):
        if np.sum(self.agent_position) == self.d * self.L:
            return True
        return False
    
class Agent:
    def __init__(self , total_actions):
        self.n = total_actions

    def choose_action(self):
        return np.random.randint(self.n)


def main(argv):
    try:
        d = int(argv[1])
        L = int(argv[2])
    except:
        d = 1
        L = 10
    
    env = Environment(d , L)
    agent = Agent(env.get_total_actions_count())

    cycle = 0

    t0 = time()
    while env.feedback() == False:
        print("\n-----------------------------------\nCycle : {0}".format(cycle))
        action_idx = agent.choose_action()
        print("Agent's Current Position: {0}".format(env.agent_position))
        print("Agent's Current Action: {0}".format(env.actions[action_idx]))
        env.interact(action_idx)
        print("Agent's New Position: {0}".format(env.agent_position))
        cycle += 1
    
    t1 = time()
    print("\nET : {0} ms".format((t1-t0)*1000))


if __name__ == "__main__":
    main(sys.argv)