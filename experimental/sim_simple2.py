import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


M = 1e6
r0 = np.array([100, 0, 0])
v0 = np.array([0, 10, 0])
state0 = np.concatenate((r0, v0))

def f(t, state):
    r = state[:3]
    v = state[3:]
    r_dot = v
    v_dot = -M*r/np.linalg.norm(r)**3
    return np.concatenate((r_dot, v_dot))


s = solve_ivp(f, (0, 2.5), state0, max_step=0.5e-4)
plt.plot(s.y[0], s.y[1])
plt.show()