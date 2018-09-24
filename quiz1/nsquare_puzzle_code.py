import numpy as np
import heapq
import copy

class Puzzle:
    def __init__(self, n:int , grid ):
        self.grid = grid
        self.n = n
        self.blank = 0
        self.goal_state_tup = tuple(range(1 , self.n**2 - 1)) + (0,0)

    def h(self , grid=None):
        if grid is None:
            grid = self.grid
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if grid[i,j] != self.blank:
                    dist += abs( grid[i,j]//self.n - i) + abs( grid[i,j] % self.n - j)

        return dist

    def add_list_in_set(self , v:set , l:list):
        v.add(tuple(l))

    def solve(self):
        open_states = []
        visited = set()

        g_start = 0
        h_start = self.h()
        f_start = g_start + h_start
        curr_state_tup = tuple(self.grid.flatten().tolist())
        item_to_push = tuple((f_start , h_start , g_start , curr_state_tup))
        heapq.heappush(open_states , item_to_push)
        previous_state = dict()
        n = self.n
        goal_reached = False
        while len(open_states) != 0 and goal_reached == False:
            f_curr , h_curr , g_curr , curr_state_tup = heapq.heappop(open_states)
            if self.goal_state_tup == curr_state_tup:
                goal_reached = True
                break
            state_curr = np.array(list(curr_state_tup) , dtype=np.int).reshape((n,n))
            if (curr_state_tup not in visited):
                visited.add(curr_state_tup)
                rL , cL = tuple(map(list , np.where(state_curr==self.blank)))
                blank_pos_list = []
                for i,j in zip(rL , cL):
                    blank_pos_list.append(tuple((i,j)))
                
                moves_list = [(1, 0), (0, 1), (-1, 0), (0, -1)] 
                for blank_curr_pos in blank_pos_list:
                    for move in moves_list:
                        blank_next_pos = (blank_curr_pos[0] + move[0] , blank_curr_pos[1] + move[1])
                        if (0 <= blank_next_pos[0] < n) and (0 <= blank_next_pos[1] < n):
                            state_next = copy.deepcopy(state_curr)
                            state_next[blank_next_pos] , state_next[blank_curr_pos] = state_next[blank_curr_pos] , state_next[blank_next_pos]
                            next_state_tup = tuple(state_next.flatten().tolist())
                            if (next_state_tup not in visited):
                                g_next = g_curr + 1
                                h_next = self.h(state_next)
                                f_next = g_next + h_next
                                item_to_push = tuple((f_next , h_next , g_next , next_state_tup))
                                heapq.heappush(open_states , item_to_push)
                                previous_state[next_state_tup] = tuple((curr_state_tup , blank_curr_pos, move))
                                
        if goal_reached == True:
            if self.goal_state_tup == tuple(self.grid.flatten().tolist()):
                print("No move required.")
            else:
                bktrace_sequence_of_moves = []
                t = previous_state[self.goal_state_tup]
                bktrace_sequence_of_moves.append(copy.deepcopy(t))
                
                while t[0] != tuple(self.grid.flatten().tolist()):
                    t =  previous_state[ bktrace_sequence_of_moves[-1][0] ]
                    bktrace_sequence_of_moves.append(copy.deepcopy(t))
                
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