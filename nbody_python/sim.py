import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G = 1

# constants
N = 4
r0 = np.array([[0, 0, 0], [50, 0, 0], [0, 50, 0], [-100, -100, 0]])
v0 = np.array([[0, 0, 0], [0, 100, 0], [-100, 0, 0], [-10, -30, 0]])
m = np.array([1e6, 1, 10000, 10])

def f(t, y):
    # [[obj1], [obj2], ...]
    # [obj1] = [rx,ry,rz, vx, vy, vz]
    y = np.reshape(y, (N, 6))
    rdot = y[:, 3:]
    vdot = np.zeros((N, 3))
    for i in range(N):
        vdot[i, :] = np.sum([m[j]*G*(y[j, :3] - y[i, :3])/(np.linalg.norm(y[j, :3] - y[i, :3]))**3 for j in range(N) if j != i], 0)
    return np.hstack((rdot, vdot)).flatten()


s = solve_ivp(f, (0,12), np.hstack((r0, v0)).flatten(), max_step=1e-2)

print(s.t)
print(s.y)


# for i in range(s.t.shape[0]):
#     if i % 10 != 0:
#         continue
#     plt.figure()
#     plt.plot(s.y[6][:i], s.y[7][:i])
#     plt.plot(s.y[0][:i], s.y[1][:i], marker='o')
#     plt.plot(s.y[12][:i], s.y[13][:i])
#     plt.plot(s.y[18][:i], s.y[19][:i])
#     plt.savefig('fig{:04d}.png'.format(i//10))
#     print(i)