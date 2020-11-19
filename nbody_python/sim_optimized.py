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
m_mat = np.array([[[m[i]]*3 for i in range(N)]]*N)  # print hem met m = np.arange(4) als je m niet snapt


def f(t, y):
    y = np.reshape(y, (N, 6))
    r = y[:, :3]
    r_mat = np.tile(r, (N, 1, 1))  # matrix where each row
    rel_pos_mat = r_mat - r_mat.transpose((1, 0, 2))
    norms_mat = (np.linalg.norm(rel_pos_mat, axis=2)**3)
    np.fill_diagonal(norms_mat, 1)
    norms_mat = norms_mat.reshape(N, N, 1).repeat(3, axis=2)
    vdot_new = np.sum(m_mat*rel_pos_mat/norms_mat, axis=1)

    rdot = y[:, 3:]
    # vdot = np.zeros((N, 3))
    # for i in range(N):
    #     vdot[i, :] = np.sum([m[j]*G*(y[j, :3] - y[i, :3])/(np.linalg.norm(y[j, :3] - y[i, :3]))**3 for j in range(N) if j != i], 0)
    #
    # print(vdot)
    # print(vdot_new)
    return np.hstack((rdot, vdot_new)).flatten()

#f(0, np.hstack((r0, v0)))
s = solve_ivp(f, (0,12), np.hstack((r0, v0)).flatten(), max_step=1e-2)
#
print(s.t)
print(s.y)
plt.plot(s.y[6], s.y[7])
plt.show()
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