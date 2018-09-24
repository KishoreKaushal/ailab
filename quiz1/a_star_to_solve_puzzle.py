#!/usr/bin/env python3


# Kaushal Kishore (bithack)
# 111601008
# quiz 1

# Coding the nsquare_minus_two_puzzle and solving by a_star

import sys
import numpy as np
from collections import deque
import heapq
import copy


# <S , A, R, T>
class Environment:
    def __init__(self, _n:int , _grid, _blank:list):
        self.n = _n                             # shape of grid
        self.grid = copy.deepcopy(_grid)        # grid passed from external environment
        self.blank = set(_blank)                # set of blank values
        self.render()

    def render(self ,n=None , grid=None , blank = None):
        if (n is None) or (grid is None) or (isinstance(blank,set)==False) or (blank is None):
            grid = self.grid
            n = self.n
            blank = self.blank

        # printing the puzzle initially
        for i in range(0,self.n):
            for j in range(0,self.n):
                if grid[i,j] in blank:
                    try:
                        print('█' ,end="\t")
                    except:
                        print('#' , end="\t")
                else:
                    print(grid[i , j] ,end="\t" )
            print("\n" , end="")


    def d(self , blank_val = None , grid_list = None):
        if grid_list is None or blank_val is None:
            blank_val = self.n**2
            grid_list = self.grid.flatten().tolist().astype(int)

        (r , c) = divmod(grid_list.index(blank_val) , self.n)
        return (self.n - r - 1 ) + (self.n - c - 1)


    def indicator(self , condition):
        if condition == True:
            return 1
        return 0

    def parity(self ,n=None , grid=None ,  blank_val=None):
        if n is None or grid is None or blank_val is None:
            n = self.n
            blank_val = n**2
            grid = copy.deepcopy(self.grid)

        accumulate_sum = 0

        # pi and pj are position index where as pi_s and pj_s are the value at that index
        grid_list = grid.flatten().tolist().astype(np.int)

        # print(grid_list)
        for pi in range(0,n*n):
            for pj in range(pi , n*n):
                accumulate_sum += self.indicator(grid_list[pj] < grid_list[pi])
        return (self.d(blank_val , grid_list)  + accumulate_sum) % 2

    def interact(self , action):
        # four actions are available : {left : 0, right:1 , up:2 , down:3}
        
        # calculating the position of the blank space
        r_blank , c_blank = divmod(self.grid.index(0) , self.n)

        if action is "LEFT" or action is 0 and c_blank > 0:
            # moving the blank space LEFT --> results in moving the left element right
            r_element , c_element = r_blank , c_blank-1

        elif action is "RIGHT" or action is 1 and c_blank < self.n-1:
            r_element , c_element = r_blank , c_blank+1
            
        elif action is "UP" or action is 2 and r_blank > 0:
            r_element , c_element = r_blank-1 , c_blank

        elif action is "DOWN" or action is 3 and r_blank < self.n-1:
            r_element , c_element = r_blank+1 , c_blank
        
        else:
            print("Invalid Action")
        
        self.grid[r_blank*self.n + c_blank] = self.grid[r_element*self.n + c_element]
        self.grid[r_element*self.n + c_element] = 0

        print("Environment After action:")
        self.render()


    def solve(self):

        pass



class Agent:
    '''
        env : Object of the Class Environment
        h   : heuristic function
    '''
    def __init__(self, env:Environment , h):
        self.env = copy.deepcopy(env)
        self.h = h
        self.goal_state = np.arange(1 , self.env.n**2 + 1).reshape(self.env.n , self.env.n).astype(int)

    # def change_parity_to_even(self):
    #     # if initial parity is odd then move the B1 and B2 in such a way that parity becomes even
    #     grid = copy.deepcopy(self.env.grid)
    #     if self.env.parity(self.env.n,grid ,blank_val) == 0:
    #         return []
    #     else:
    #         pass


    def path_search(self):
        # unlike BFS where we used FIFO-queue, we will be using priority queue (min-heap)
        openStates = []

        # creating a set for the explored coordinates
        visited = set()     # visited set

        # creating a array for the g(n)
        g = dict()
        g[str(self.env.grid.flatten().tolist())] = 0
        
        # g = np.ones_like(self.env.grid) * float("inf")
        # g[self.env.agent_position] = 0

        # pushing the starting position into the heap
        heapq.heappush( openStates , tuple([ self.h(self.env.grid ,  self.goal_state), np.random.randn() , copy.deepcopy(self.env.grid) ]))

        # creating a cameFrom set : it'll be used for reconstructing the path sequence
        _r , _c = self.env.grid.shape
        cameFrom = dict()
        cameFrom[str(self.env.grid.flatten().tolist())] = ("START" , "START" )


        goal_reached = False

        # to limit the search for `cycle` number of steps
        cycle = 100000

        while len(openStates) != 0 and goal_reached == False and cycle>0:
            # pop an element from the  min heap having lowest f-score
            current = heapq.heappop(openStates)[2]
            print(current)
            # if goal is reached
            if np.sum(current !=  self.goal_state) == 0:
                goal_reached = True
                break

            blank_pos = []
            for i in self.env.blank:
                blank_pos.append(tuple(map(int , np.where(current ==  i))))

            # if the current coordinate is not explored
            
            if (str(current.flatten().tolist()) not in visited):
                # mark and explore the current coordinate
                visited.add(str(current.flatten().tolist()))

                for bidx in range(len(blank_pos)): 
                    # since it is a grid problem, therefore, there are four adjacent nodes : L,R,U,D
                    # for both of the blanks
                    # LEFT    
                    # get the next state on moving left the blank0
                    
                    next_state = copy.deepcopy(current)
                    currentpos_of_blank = blank_pos[bidx]
                    nextpos_of_blank = ( currentpos_of_blank[0] , currentpos_of_blank[1] - 1)
                    # if this coodinate is valid
                    if (nextpos_of_blank[1] >= 0):
                        # move the blank to new position
                        temp = next_state[currentpos_of_blank]
                        next_state[currentpos_of_blank] = next_state[nextpos_of_blank]
                        next_state[nextpos_of_blank] = temp

                        # if next_state is not explored yet
                        if (str(next_state.flatten().tolist()) not in visited):
                            # update the g(n) for the nextpos
                            g[str(next_state.flatten().tolist())] = g[str(current.flatten().tolist())] + 1
                            # calculate the f-score by using heuristics 
                            f_nextpos = g[str(next_state.flatten().tolist())] + self.h(next_state , self.goal_state)
                            print("F : ", f_nextpos)
                            # push this information into the min-heap
                            t = copy.deepcopy(next_state)
                            heapq.heappush(openStates , tuple([ f_nextpos ,np.random.randn() ,  t]))
                            # add the information about the parent coodinate position in the cameFrom array
                            # cameFrom array will be used to reconstruct the path in the next step
                            cameFrom[str(next_state.flatten().tolist())] = (str(current.flatten().tolist()) , "Move BlankIdx: {0} LEFT".format(bidx))

                    # RIGHT
                    # the procedure is same as in above step
                    next_state = copy.deepcopy(current)
                    currentpos_of_blank = blank_pos[bidx]
                    nextpos_of_blank = ( currentpos_of_blank[0] , currentpos_of_blank[1] + 1)
                    if (nextpos_of_blank[1] < _c):
                        # move the blank to new position
                        temp = next_state[currentpos_of_blank]
                        next_state[currentpos_of_blank] = next_state[nextpos_of_blank]
                        next_state[nextpos_of_blank] = temp
                        # if next_state is not explored yet
                        if (str(next_state.flatten().tolist()) not in visited):
                            # update the g(n) for the nextpos
                            g[str(next_state.flatten().tolist())] = g[str(current.flatten().tolist())] + 1
                            # calculate the f-score by using heuristics 
                            f_nextpos = g[str(next_state.flatten().tolist())] + self.h(next_state , self.goal_state)
                            # push this information into the min-heap
                            t = copy.deepcopy(next_state)
                            heapq.heappush(openStates , tuple([ f_nextpos ,np.random.randn(),  t]))
                            # add the information about the parent coodinate position in the cameFrom array
                            # cameFrom array will be used to reconstruct the path in the next step
                            cameFrom[str(next_state.flatten().tolist())] = (str(current.flatten().tolist()) , "Move BlankIdx: {0} RIGHT".format(bidx))

                    # UP

                    next_state = copy.deepcopy(current)
                    currentpos_of_blank = blank_pos[bidx]
                    nextpos_of_blank = ( currentpos_of_blank[0] -1 , currentpos_of_blank[1])
                    # if this coodinate is valid
                    if (nextpos_of_blank[0] >= 0):
                        # if next_state is not explored yet
                        if (str(next_state.flatten().tolist()) not in visited):
                            # update the g(n) for the nextpos
                            g[str(next_state.flatten().tolist())] = g[str(current.flatten().tolist())] + 1
                            # calculate the f-score by using heuristics 
                            f_nextpos = g[str(next_state.flatten().tolist())] + self.h(next_state , self.goal_state)
                            # push this information into the min-heap
                            t = copy.deepcopy(next_state)
                            heapq.heappush(openStates , tuple([ f_nextpos ,np.random.randn(),  t]))
                            # add the information about the parent coodinate position in the cameFrom array
                            # cameFrom array will be used to reconstruct the path in the next step
                            cameFrom[str(next_state.flatten().tolist())] = (str(current.flatten().tolist()) , "Move BlankIdx: {0} UP".format(bidx))

                    # DOWN
                    next_state = copy.deepcopy(current)
                    currentpos_of_blank = blank_pos[bidx]
                    nextpos_of_blank = ( currentpos_of_blank[0] +1 , currentpos_of_blank[1])
                    # if this coodinate is valid
                    if (nextpos_of_blank[0] < _r):
                        # if next_state is not explored yet
                        if (str(next_state.flatten().tolist()) not in visited):
                            # update the g(n) for the nextpos
                            g[str(next_state.flatten().tolist())] = g[str(current.flatten().tolist())] + 1
                            # calculate the f-score by using heuristics 
                            f_nextpos = g[str(next_state.flatten().tolist())] +self.h(next_state , self.goal_state)
                            # push this information into the min-heap
                            t = copy.deepcopy(next_state)
                            heapq.heappush(openStates , tuple([ f_nextpos ,np.random.randn(),  t]))
                            # add the information about the parent coodinate position in the cameFrom array
                            # cameFrom array will be used to reconstruct the path in the next step
                            cameFrom[str(next_state.flatten().tolist())] = (str(current.flatten().tolist()) , "Move BlankIdx: {0} DOWN".format(bidx))

            cycle-=1
        

        print (cameFrom)

        if goal_reached == True:
            # reconstructing the path using backtracing
            path = [str(self.goal_state.flatten().tolist())]

            while True:
                s = path[-1]
                if s == "START":
                    break
                if s in cameFrom.keys():
                    path.append(cameFrom[s][1])

            print("Sequence of Moves...\n")
            
            while len(path) != 0:
                print(path.pop(-1))


def manhattan_distance(arr1 , arr2):
    return np.sum(np.abs(arr1-arr2))

def main():
    n = int(input("Enter n: "))
    blank = [n*n - 1 , n*n]
    print("Assuming blanks value respectively as: {0}".format(blank))
    grid = []

    for i in range(n):
        temp = input("Enter row {0} : ".format(i+1)).strip().split(' ')
        temp = list(map(int ,list(filter(str.strip , temp))))
        grid.append(temp)

    grid = np.array(grid, dtype=np.int)
    # print(grid)

    env = Environment(n,grid,blank)
    agent = Agent(env , manhattan_distance)
    agent.path_search()



if __name__ == "__main__":
    main()