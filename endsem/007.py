from __future__ import print_function
import numpy as np
import copy


class Solution:

    def __init__(self, gamma=0.9):

        self.v = np.zeros((20, 10, 10))
        self.gamma = gamma
        self.fact = self.generate_factorials()
        self.actions = self.generate_actions()
        self.states = self.generate_states()
        self.optimalAction = [[[0 for _ in range(20)] for _ in range(10)] for _ in range(10)]
        self.A = len(self.actions)
        self.pro1, self.pro2, self.left1, self.left2 = self.generate_probabilities()

    def generate_probabilities(self):

        pro1 = np.zeros((25, 3))
        pro2 = np.zeros((25, 3))
        left1 = np.zeros((25, 3))
        left2 = np.zeros((25, 3))

        sum1 = np.zeros(3)
        sum2 = np.zeros(3)

        l1 = [3, 2, 2]
        l2 = [3, 1, 1]

        for i in range(0, 20):
            for j in range(0, 3):
                p1 = self.poisson(i, l1[j])
                p2 = self.poisson(i, l2[j])
                pro1[i, j] = p1
                pro2[i, j] = p2
                sum1[j] += p1
                sum2[j] += p2
                left1[i, j] = sum1[j]
                left2[i, j] = sum2[j]
        return pro1, pro2, left1, left2

    @staticmethod
    def generate_factorials(n=30):

        fact = np.zeros(n + 1)
        fact[0] = 1
        for i in range(1, n + 1):
            fact[i] = i * fact[i - 1]
        return fact

    def generate_states(self):

        states = []
        for s1 in range(0, 20):
            for s2 in range(0, 10):
                for s3 in range(0, 10):
                    states.append((s1, s2, s3))
        return states

    @staticmethod
    def generate_actions():

        actions = []

        # f1, g1 - 2, 3
        # f2, g2 - 1, 3
        # f3, g3 - 1, 2

        for f1 in range(0, 5):
            for g1 in range(0, 5 - f1):
                for f2 in range(0, 5):
                    if f1 and f2: continue
                    for g2 in range(0, 5 - f2):
                        for f3 in range(0, 5):
                            if f3 and g1: continue
                            for g3 in range(0, 5 - f3):
                                if g2 and g3: continue
                                actions.append((f1, g1, f2, g2, f3, g3))

        return actions

    def poisson(self, n, lamb):

        return pow(lamb, n) / self.fact[n] * np.exp(-lamb)

    @staticmethod
    def inf_norm(a):

        return np.linalg.norm(a, ord='inf')

    def generate_new_states(self, sn1, sn2, sn3, cn1, cn2, cn3):
        next_states = []
        for l1 in range(0, sn1):
            for l2 in range(0, sn2):
                for l3 in range(0, sn3):
                    for e1 in range(0, cn1):
                        for e2 in range(0, cn2):
                            for e3 in range(0, cn3):
                                next_states.append((l1, l2, l3, e1, e2, e3))
        return next_states

    def value_iteration(self, v):

        new_v = copy.deepcopy(v)
        optimalAct = None

        for state in self.states:
            print (state)
            s1, s2, s3 = state
            maxv = -np.inf

            for action in self.actions:
                f1, g1, f2, g2, f3, g3 = action
                if f1 + g1 > s1 or f2 + g2 > s2 or f3 + g3 > s3:
                    continue
                sn1 = s1 - f1 - g1 + f2 + f3
                sn2 = s2 - f2 - g2 + f1 + g3
                sn3 = s3 - f3 - g3 + g1 + g2
                reward = (f1 + g1 + f2 + g2 + f3 + g3) * -2

                next_states = self.generate_new_states(sn1, sn2, sn3, 19, 9, 9)
                res = reward

                for next_state in next_states:
                    l1, l2, l3, e1, e2, e3 = next_state
                    p1 = self.pro1[l1, 0] * self.pro1[l2, 1] * self.pro1[l3, 2]
                    p2 = self.pro2[e1, 0] * self.pro2[e2, 1] * self.pro2[e3, 2]
                    fn1 = min(19, sn1 - l1 + e1)
                    fn2 = min(9, sn2 - l2 + e2)
                    fn3 = min(9, sn3 - l3 + e3)
                    res = res + p1 * p2 * (10 * (l1 + l2 + l3) + self.gamma * v[fn1, fn2, fn3])

                if res > maxv:
                    maxv = res
                    optimalAct = action

            new_v[state] = maxv
            self.optimalAction = optimalAct

        return new_v

    def run(self, epsilon=0.1):
        cnter = 0
        while True:
            print(cnter)
            new_v = self.value_iteration(self.v)
            if self.inf_norm(self.v - new_v) < epsilon:
                break
            cnter += 1


epsilon = 0.1
gamma = 0.9

env = Solution(gamma)
env.run(epsilon)
