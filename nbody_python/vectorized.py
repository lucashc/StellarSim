import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# constants
N = 2
r0 = np.array([[0, 0, 0], [100, 100, 0]])
v0 = np.array([[0, 0, 0], [10, 0, 0]])
m = np.array([1e6, 1])


def f(t, y):
    rdot = y[0,:]
    r = y[1,:]
    vdot = np.sum(m*G*())
    # # [[obj1], [obj2], ...]
    # # [obj1] = [rx,ry,rz, vx, vy, vz]
    # y = np.reshape(y, (N, 6))
    # rdot = y[:, 3:]
    # vdot = np.zeros((N, 3))
    # for i in range(N):
    #     vdot[i, :] = np.sum([m[j]*G*(y[j, :3] - y[i, :3])/(np.linalg.norm(y[j, :3] - y[i, :3]))**3 for j in range(N) if j != i], 0)
    # return np.hstack((rdot, vdot)).flatten()


f = np.vectorize(f)

s = solve_ivp(f, (0,100), np.hstack((r0, v0)).flatten(), max_step=1)

print(s.t)
print(s.y)


plt.plot(s.y[6], s.y[7])
plt.show()