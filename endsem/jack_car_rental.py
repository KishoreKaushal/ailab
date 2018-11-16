import numpy as np
import copy
import itertools
from scipy.stats import poisson
import time

class Environment:
    def __init__(self):
        # dynamics of the MDP process for Jack-Car rental Problem
        self.number_of_locations = 3
        self.rental_credit = 10
        self.expected_rental_requests = [3, 2, 2]
        self.expected_rental_returns = [3, 1, 1]
        self.capacity = [5, 3, 3]
        self.max_car_moved = 2
        self.gamma = 0.9
        self.cost_of_moving = [2, 0, 2]

        # available actions : actions can be accessed through the index
        self.actions = [i for i in itertools.product(range(-self.max_car_moved, self.max_car_moved+1),
                                                     range(-self.max_car_moved, self.max_car_moved+1),
                                                     range(-self.max_car_moved, self.max_car_moved+1))]

        # available states : available states can be accessed through the index
        self.states = [i for i in itertools.product(range(self.capacity[0]+1),
                                                    range(self.capacity[1]+1),
                                                    range(self.capacity[2]+1))]

        # initializing the values of the states
        self.V = np.zeros(tuple(np.array(self.capacity) + 1), dtype=np.float)

        # initializing the policy array
        self.policy = np.zeros(tuple(np.array(self.capacity) + 1), dtype=np.int)
        
        # poisson precompute
        self.poisson_pmf = dict()
        self.poisson_sf = dict()
        
        for n , lam in itertools.product(range(-1 , max(self.capacity) + 1), 
                                         range(max(self.expected_rental_requests + self.expected_rental_returns)+1)):
            self.poisson_pmf[(n,lam)] = poisson.pmf(n,lam)
            self.poisson_sf[(n,lam)] = poisson.sf(n,lam)
        
                
        
        # printing the dynamics
        self.print_dynamics()
        
    def print_dynamics(self):
        print("Total Number of Locations: " , self.number_of_locations)
        print("Rental Credit: ", self.rental_credit)
        print("Expected Rental Requests: ", self.expected_rental_requests)
        print("Expected Rental Returns: ", self.expected_rental_returns)
        print("Capacity: " , self.capacity)
        print("Discount Factor: ", self.gamma)
        print("Cost of Moving: ", self.cost_of_moving)
        print("Total number of actions: " , len(self.actions))
        print("Total number of states: ", len(self.states) )


    
    def expected_return(self, state, action):
        # initiate and populate returns with cost associated with moving cars
        returns = 0.0
        returns -= np.sum(np.multiply(self.cost_of_moving , np.abs(action)))
        # number of cars to start the day
        # cars available at a location:
        # current number of car - number of cars exit + number of cars return
        cars_available = [min(state[0] - action[0] + action[2], self.capacity[0]),
                          min(state[1] - action[1] + action[0], self.capacity[1]),
                          min(state[2] - action[2] + action[1], self.capacity[2])]
        
        # iterate over all rental rates combinations: (rental_loc0 , rental_loc1 , rental_loc2)
        for rental_rates in itertools.product(range(cars_available[0]+1),
                                              range(cars_available[1]+1),
                                              range(cars_available[2]+1)):
            # finding the rental probabilities: probability of occurring this event
            # rental probability = 
            # p(rental rate of location 0) * p(rental rate of location 1) * p(rental rate of location 2)
            temp = [int(rental_rates[i]==cars_available[i]) for i in range(len(rental_rates))]
            
            prob = [round(self.poisson_pmf[(rental_rates[i] , self.expected_rental_requests[i])] * (1-temp[i])
                          + self.poisson_sf[(rental_rates[i]-1 , self.expected_rental_requests[i])] * (temp[i]) , 3)
                    for i in range(len(rental_rates))]

            rental_prob = np.prod(prob)
            
            # total rentals: number of car that can be rented given a request
            total_rentals = [min(cars_available[i] , rental_rates[i]) for i in range(len(rental_rates))]
            # total rewards
            current_rental_rewards = self.rental_credit * np.sum(total_rentals)
            
            # iterate over all return rate combinations: (return_loc0 , return_loc1 , return_loc2)
            for return_rates in itertools.product(range(self.capacity[0]+1),
                                                  range(self.capacity[1]+1),
                                                  range(self.capacity[2]+1)):
                # finding the return rate probabilities: probability of occurring this event
                # return priobability = 
                # p(return rate of location 0) * p(return rate of location 1) * p(return rate of location 2)
                temp = [int(return_rates[i]==self.capacity[i]) for i in range(len(return_rates))]
                
                prob = [round(self.poisson_pmf[(return_rates[i] , self.expected_rental_returns[i])] * (1-temp[i])
                              + self.poisson_sf[(return_rates[i]-1 , self.expected_rental_returns[i])] * (temp[i]) , 3)
                        for i in range(len(return_rates))]
                return_prob = np.prod(prob)
                current_return_prob = rental_prob * return_prob
                
                # number of cars at the end of the day
                cars_available_eod = [min(cars_available[i] - rental_rates[i] + return_rates[i] , self.capacity[i])
                                        for i in range(len(return_rates))]
                # increment the return
                returns += current_return_prob * (current_rental_rewards + self.gamma * self.V[tuple(cars_available_eod)])

        return returns

    def value_iteration(self, threshold=0.1):
        # no need to copy, because its going to converge in each value iterations
        V = self.V
        # copy for safety
        actions = copy.deepcopy(self.actions)
        states = copy.deepcopy(self.states)
        
        iteration = 0
        while True:
            delta = 0
            # for all the states
            for state_idx, state in enumerate(states):
                print("State_idx: " , state_idx)
                # state : (car in loc0 , car in loc1, car in loc2)
                v = V[state]
                # assign V[state] = max( expected return for choosing an action a from all possible actions)
                # possible actions : so that the cars_available must not be less than equal to zero at any location
                V[state] = -np.inf
                for action_idx , action in enumerate(actions):
                    #print("Action_idx: " , action_idx)
                    next_state = np.array([state[0] - action[0] + action[2],
                                           state[1] - action[1] + action[0],
                                           state[2] - action[2] + action[1]])
                    # if the next state is valid then the action is possible for this state
                    if np.all(next_state > 0):
                        #t0 = time.time()
                        expected_return_from_this_state = self.expected_return(state, action)
                        #t1 = time.time()
                        #print("time taken: {} seconds".format(t1-t0))
                        if expected_return_from_this_state > V[state]:
                            V[state] = expected_return_from_this_state
                
                delta = max(delta , abs(v-V[state]))
            
            iteration += 1
            print("Iteration: {}\tDelta: {}".format(iteration , delta))
            if delta <= threshold:
                break
            

def main():
    jack_car_rental = Environment()
    jack_car_rental.value_iteration()
    #value_fname = "value.txt"
    #policy_fname = "policy.txt"
    #print("Value array saving to file: {}".format(value_fname))
    #print("Policy array saving to file: {}".format(policy_fname))
    
if __name__ == "__main__":
    main()
