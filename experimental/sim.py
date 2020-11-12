import numpy as np
from scipy.constants import G
from scipy.integrate import RK45
# constants
N = 2
r0 = np.array([[0, 0, 0], [100, 100, 0]])
v0 = np.array([[0, 0, 0], [-1, -1, 0]])
m = np.array([1e6, 1])


def g_acc(t, r):
    return np.sum([m[j]*G*(r[j] - r)/(np.linalg.norm(r[j] - r))**3 for j in range(N) if r[j] != r], 0)


RK45(g_acc, (0, 10), r0)

