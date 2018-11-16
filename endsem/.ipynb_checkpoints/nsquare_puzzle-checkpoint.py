import sys
import numpy as np
from collections import deque
import heapq
import copy

class Puzzle:
    def __init__(self, n:int , grid ):
        self.grid = grid
        self.n = n
        self.blank = 0
        # self.goal_state_tup = tuple(range(1 , self.n**2 - 1)) + (0,0)
        self.goal_state_tup = tuple()

    def h(self , grid=None):
        if grid is None:
            grid = self.grid
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if grid[i,j] != self.blank:
                    dist += abs( (grid[i,j]-1)//self.n - i) + abs( (grid[i,j]-1) % self.n - j)

        return dist

    def add_list_in_set(self , v:set , l:list):
        v.add(tuple(l))

    def solve(self):
        # priority queue
        # each object in the heap openStates will be in the format:
        # tuple(f:int , h:int , g:int , tuple([....])) 
        # where f = g + h , and g(s) and h(s) have their usual meanings
        # tuple([....]) : is the state of the n-puzzle
        open_states = []

        # creating a set for the explored states
        visited = set()

        # pushing the starting position into the heap
        g_start = 0
        h_start = self.h()
        f_start = g_start + h_start
        curr_state_tup = tuple(self.grid.flatten().tolist())
        item_to_push = tuple((f_start , h_start , g_start , curr_state_tup))
        heapq.heappush(open_states , item_to_push)

        # creating a previous state dictionary for moves reconstruction
        # each element in this dictionary will be of form:
        # key:tuple -> ( previous_state:tuple , (r:int , c:int):tuple , move:tuple ):tuple
        previous_state = dict()

        n = self.n

        goal_reached = False

        
        while len(open_states) != 0 and goal_reached == False:
            # pop and unpack an element from the min heap having the highest priority
            f_curr , h_curr , g_curr , curr_state_tup = heapq.heappop(open_states)

            # check if this is the goal
            if self.goal_state_tup == curr_state_tup:
                goal_reached = True
                break

            # converting to numpy array format
            state_curr = np.array(list(curr_state_tup) , dtype=np.int).reshape((n,n))

            # if this state is not explored yet
            if (curr_state_tup not in visited):
                # mark and explore the current state
                visited.add(curr_state_tup)

                # finding the blank positions coordinates
                rL , cL = tuple(map(list , np.where(state_curr==self.blank)))
                blank_pos_list = []
                for i,j in zip(rL , cL):
                    blank_pos_list.append(tuple((i,j)))
                
                # since it is a grid problem, therefore, at any time we can move a blank space : LEFT, RIGHT, UP, DOWN

                # generating moves
                # down  => (1, 0)
                # right => (0, 1) 
                # up    => (-1, 0) 
                # left  => (0, -1)

                # can be generated like this:
                # moves_list = list(map(tuple,np.vstack((np.eye(2,dtype=np.int),-1*np.eye(2 , dtype=np.int))).tolist()))
                
                # but because of small list we hardcode the moves for speed
                moves_list = [(1, 0), (0, 1), (-1, 0), (0, -1)] 

                # for each blank_position
                for blank_curr_pos in blank_pos_list:
                    for move in moves_list:
                        blank_next_pos = (blank_curr_pos[0] + move[0] , blank_curr_pos[1] + move[1])

                        # if next_position of the blank is valid
                        if (0 <= blank_next_pos[0] < n) and (0 <= blank_next_pos[1] < n):
                            # swap the element at those positions to get the next state
                            # first make a deepcopy of the current grid to avoid any data hazard
                            state_next = copy.deepcopy(state_curr)
                            # print(state_next , blank_next_pos , blank_curr_pos)
                            state_next[blank_next_pos] , state_next[blank_curr_pos] = state_next[blank_curr_pos] , state_next[blank_next_pos]
                            
                            next_state_tup = tuple(state_next.flatten().tolist())
                            
                            if (next_state_tup not in visited):
                                # we got the next state lets proceed with the cost calculation using heuristic function
                                g_next = g_curr + 1
                                h_next = self.h(state_next)
                                f_next = g_next + h_next
                                item_to_push = tuple((f_next , h_next , g_next , next_state_tup))
                                # push into the heap
                                heapq.heappush(open_states , item_to_push)

                                previous_state[next_state_tup] = tuple((curr_state_tup , blank_curr_pos, move))

        # goal is reachable in every case
        if goal_reached == True:
            if self.goal_state_tup == tuple(self.grid.flatten().tolist()):
                print("No move required.")
            else:
                # reconstruct the sequence of moves
                bktrace_sequence_of_moves = []
                # start the bktrace from the goal state and moving backwards
                t = previous_state[self.goal_state_tup]
                bktrace_sequence_of_moves.append(copy.deepcopy(t))
                
                while t[0] != tuple(self.grid.flatten().tolist()):
                    t =  previous_state[ bktrace_sequence_of_moves[-1][0] ]
                    bktrace_sequence_of_moves.append(copy.deepcopy(t))
                total_moves = 0
                while len(bktrace_sequence_of_moves) != 0:
                    elem = bktrace_sequence_of_moves.pop(-1)
                    arr  = np.array(list(elem[0])).reshape(n , -1)
                    if elem[2] == (1,0):
                        dirn = "DOWN"
                    elif elem[2] == (0,1):
                        dirn = "RIGHT"
                    elif elem[2] == (-1,0):
                        dirn = "UP"
                    else:
                        dirn = "LEFT"
                    print("{0} \n Move the blank Position at {1} to {2}".format(arr , elem[1] , dirn))
                    total_moves+=1
                
                print("\nWe are gonna win this war. Total Moves Taken: {0}".format(total_moves))


def main():
    n = int(input("Enter n: "))
    print("Representing the blanks as: 0")
    grid = []
    for i in range(n):
        temp = input("Enter row {0} : ".format(i+1)).strip().split(' ')
        temp = list(map(int ,list(filter(str.strip , temp))))
        grid.append(temp)

    grid = np.array(grid, dtype=np.int)
    puzzle = Puzzle(n , grid)
    puzzle.solve()

if __name__=="__main__":
    main()