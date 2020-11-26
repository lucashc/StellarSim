import numpy as np
from random import uniform
import matplotlib.pyplot as plt
from tqdm import tqdm


points = np.linspace(2, 100, 50)

def gp(r, a):
    return 0.001/(r-a)**2

def dp(r):
    return 1/r

def diff(p, loc):
    diffs = 0
    for r in p:
        diffs += abs(sum([gp(r, l) for l in loc])-dp(r))
    return diffs

loc = [0]

current = diff(points, loc)

for i in tqdm(range(1000)):
    a = uniform(1, 100)
    res = diff(points, loc+[a])
    if res < current:
        current = res
        loc += [a]


plt.plot(points, dp(points))



value = sum([gp(points, l) for l in loc])
plt.plot(points, value)
plt.show()

ppoints = np.linspace(2, 100, 333)

d = [abs(sum([gp(r, l) for l in loc])-dp(r)) for r in ppoints]
d.sort()
print(d)

plt.hist(d[:300])
plt.show()