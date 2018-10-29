from __future__ import print_function
import numpy as np
import copy

# in lines around 85
# make the simulate parameter True to print iterations. it is recommened that the value of
# iterations should be reduced.

eps = 1e-6
gamma = 1.0 #0.99
wickets = 3
overs = 10
economy = [3, 3.5, 4, 4.5, 5]
strike = [33, 30, 24, 18, 15]

for i in strike:
    print (6 / i)

v = np.zeros((overs + 1, wickets + 1, (1 << 10)))
a = np.zeros((overs + 1, wickets + 1, (1 << 10)), dtype = np.int32)

def binary(n):
    ans = ''
    for i in range(0, 10):
        if n & (1 << i):
            ans += '1'
        else:
            ans += '0'
    #new_ans = ans[:: -1]
    return ans


def simulate(can_print = True):
    # val = calc_dp(10, 0, int((1 << 10) - 1))
    global a
    value = 0
    wickets = 0
    mask = (1 << 10) - 1

    if can_print: print ('i', 'random', 'wickets', 'mask', 'bowler')

    for i in range(10, 0, -1):
        if wickets == 3:
            break
        bowler = a[i][wickets][mask]
        rv = np.random.random()
        wickets += (rv < 6 / strike[bowler // 2])
        mask = mask ^ (1 << bowler)
        value += economy[bowler // 2]
        if can_print: print (i, rv, wickets, binary(mask), bowler // 2)

    if can_print: print ('value = ', value)
    return value



def initial():
    def calc_dp(overs, wickets, mask):

        if overs == 0 or wickets == 3:
            return 0
        if v[overs, wickets, mask]:
            return v[overs, wickets, mask]

        index = -1
        smin = np.inf

        for i in range(0, 10):

            nmask = mask ^ (1 << i)
            if (mask & (1 << i)):

                p = 6 / strike[i // 2]
                cur = economy[i // 2] + gamma * (p * calc_dp(overs - 1, wickets + 1, nmask) + (1 - p) * calc_dp(overs - 1, wickets, nmask))
                if cur < smin:
                    smin = cur
                    index = i

        v[overs, wickets, mask] = smin
        a[overs, wickets, mask] = index
        return smin

    val = calc_dp(10, 0, int((1 << 10) - 1))
    print (val)

    iterations = 5
    total = 0

    for i in range(0, iterations):
        #print ('')
        nv = simulate()
        total += nv

    print (total / iterations)


initial()



