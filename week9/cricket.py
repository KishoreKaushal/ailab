from __future__ import print_function
import numpy as np
import copy

scores = [1, 2, 3, 4, 6]
pw_min = [0.01, 0.02, 0.03, 0.1, 0.3]
pw_max = [0.1, 0.2, 0.3, 0.5, 0.7]
balls = 300
total_wickets = 10
pr_min = 0.5
pr_max = 0.8
shots = 5

v = np.zeros((balls + 1, total_wickets + 1))
actions = copy.deepcopy(v)

def pw (shot, wickets):
	return pw_max[shot] + (pw_min[shot] - pw_max[shot]) * (wickets - 1) / 9

def pr (wickets):
	return pr_min + (pr_max - pr_min) * (wickets - 1) / 9

def getv (b, w):
	if b < 300 and w < total_wickets:
		return v[b][w]
	else:
		return 0

for b in range(balls - 1, -1, -1):
	for w in range(total_wickets - 1, -1, -1):
		maxv = -np.inf
		actv = -1
		for s in range(0, shots):
			cpw = pw(s, total_wickets - w)
			cpr = pr(total_wickets - w)
			cur = (1 - cpw) * (cpr * scores[s] + getv(b + 1, w)) + cpw * getv(b + 1, w + 1)
			if cur > maxv:
				maxv = cur
				actv = s
		v[b][w] = maxv
		actions[b][w] = scores[actv]

np.savetxt('actions.txt', actions, fmt = '%.0f')
np.savetxt('v.txt', v, fmt = '%.1f')
