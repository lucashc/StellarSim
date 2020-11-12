import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

M = 1e6

G = 1

r = np.array([100, 0, 0])
v = np.array([0, 10, 0])
m = 1

def f(t, y):
    r = y[:3]
    v = y[3:]
    rdot = v
    vdot = -m*M*G*r/np.linalg.norm(r)**3
    return np.hstack((rdot, vdot))

s = solve_ivp(f, (0,60), np.hstack((r, v)), )
print(s.t)
print(s.y)
plt.plot(s.y[0], s.y[1])
plt.show()