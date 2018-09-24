import numpy as np
import heapq
import copy

class Puzzle:
	def __init__(self,n:int,grid):
		self.grid = grid
		self.n = n
		self.blank = 0
		self.goal_state_tup = tuple(range(1,self.n**2-1)) + (0,0)

	def h(self,grid=None):
		if grid is None:
			grid = self.grid
		accumulate = 0
		for i in range(self.n):
			for j in range(self.n):
				if grid[i,j] is not self.blank:
					accumulate  += np.abs((grid[i,j] - 1)//self.n-i) + np.abs((grid[i,j]-1)%self.n - j)
		return accumulate

	def solve_puzzle(self):
		state_priority_queue = []
		visited = set()

		g = 0
		h = self.h()
		f = g + h
		curr_state_tup = tuple(self.grid.flatten().tolist())
		heapq.heappush(state_priority_queue,tuple((f , h, g, curr_state_tup)))		

		came_from_state = dict()

		is_goal_reached = False

		print("Please calm down. Men at work.")

		while len(state_priority_queue) is not 0 and is_goal_reached is False:
			_,_,g_curr,curr_state_tup = heapq.heappop(state_priority_queue)

			if self.goal_state_tup == curr_state_tup:
				is_goal_reached = True
				break

			state_curr_mat = np.array(list(curr_state_tup), dtype=np.int).reshape((n,n))
			if curr_state_tup not in visited:
				visited.add(curr_state_tup)
				rL ,cL = tuple(map(list,np.where(state_curr_mat == self.blank)))
				list_of_blank_positions = []
				for i ,j in zip(rL,cL):
					list_of_blank_positions.append(tuple((i,j)))

			list_of_moves = [(1,0),(0,1),(-1,0),(0,-1)]

			for curr_pos_of_a_bl in list_of_blank_positions:
				for move in list_of_moves:
					next_pos_of_blank = ( curr_pos_of_a_bl[0] + move[0], curr_pos_of_a_bl[1] + move[1])

					if (0<= next_pos_of_blank[0] < n) and (0<= next_pos_of_blank[1] < n):
						next_state_mat = copy.deepcopy(state_curr_mat)
						next_state_mat[next_pos_of_blank], next_state_mat[curr_pos_of_a_bl] = next_state_mat[curr_pos_of_a_bl], next_state_mat[next_pos_of_blank]
						next_state_tup = tuple(next_state_mat.flatten().tolist())

						if (next_state_tup not in visited):
							g_next =  g_curr+ 1
							h_next = self.h(next_state_mat)
							f_next = g_next + h_next
							heapq.heappush(state_priority_queue,tuple((f_next , h_next , g_next , next_state_tup)))

							came_from_state[next_state_tup] = tuple((curr_state_tup,curr_pos_of_a_bl,move))


		if is_goal_reached is True:
			if self.goal_state_tup == tuple(self.grid.flatten().tolist()):
				print("Already in goal state")
			else:
				bktrace_sequence_of_moves = []
				z = came_from_state[self.goal_state_tup]
				bktrace_sequence_of_moves.append(copy.deepcopy(z))

				while z[0] != tuple(self.grid.flatten().tolist()):
					z = came_from_state[bktrace_sequence_of_moves[-1][0]]
					bktrace_sequence_of_moves.append(copy.deepcopy(z))

				count_total_moves = 0
				while len(bktrace_sequence_of_moves) != 0:
					popcorn = bktrace_sequence_of_moves.pop(-1)
					arr = np.array(list(popcorn[0])).reshape(n,-1)
					if popcorn[2] == (1,0):
						direction = "Down"
					elif popcorn[2] == (0,1):
						direction = "Right"
					elif popcorn[2] == (-1,0):
						direction = "Up"
					else:
						direction = "Left"

					print("{0} \n Move the Blank positioned at {1} to {2}".format(arr , popcorn[1] , direction))
					count_total_moves+=1

				print(np.array(list(self.goal_state_tup), dtype=np.int).reshape((n,n)))

				print("\nTotal Moves Taken: {0}".format(count_total_moves))


n = int(input("Enter Puzzle Size n: "))
print("Considering the blank as 0.")
grid = []
for i in range(n):
	temp = input("Row {0} : ".format(i+1)).strip().split(' ')
	temp = list(map(int,list(filter(str.strip,temp))))
	grid.append(temp)
grid = np.array(grid , dtype=np.int)
puzzle = Puzzle(n,grid)
puzzle.solve_puzzle()