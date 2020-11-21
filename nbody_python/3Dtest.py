import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm, colors, animation
import time

G = 1

# constants
# N = 2
# r0 = np.array([[-50, 0, 0], [50, 0, 0]], dtype=np.double)
# v0 = np.array([[0, -0.7, 0], [0, 0.7, 0]], dtype=np.double)
# m = np.array([100, 100], dtype=np.double)
N = 4
r0 = np.array([[0, 0, 0], [50, 0, 0], [0, 50, 0], [-100, -100, 0]], dtype=np.double)
v0 = np.array([[0, 0, 0], [0, 100, 50], [-100, 0, 20], [-10, -30, 0]], dtype=np.double)
m = np.array([1e6, 1, 10000, 10], dtype=np.double)
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
s = solve_ivp(f, (0,20), np.hstack((r0, v0)).flatten(), max_step=1e-2)
#

until_timestep = int(1e5)
large_limits = {"xlim": (-200, 200), "ylim": (-200, 200), "zlim":(-200, 200)}
sun_limits = {"xlim": (-20, 1), "ylim": (-10, 10), "zlim": (-1, 5)}
starting_angle = 270  # default 270, 0 for sun zoom
rotation_speed = 40  # default 40
elevation = 0  # default 0
def data_gen(index):
    ax.clear()
    #ax.axis('off')
    ax.grid('off')
    plot0 = ax.plot3D(s.y[0][:index], s.y[1][:index], s.y[2][:index], linewidth=2)
    plot1 = ax.plot3D(s.y[6][:index], s.y[7][:index], s.y[8][:index])
    plot2 = ax.plot3D(s.y[12][:index], s.y[13][:index], s.y[14][:index])
    plot3 = ax.plot3D(s.y[18][:index], s.y[19][:index], s.y[20][:index])
    ax.set(**large_limits)
    ax.view_init(elev=elevation, azim=index/until_timestep*rotation_speed + starting_angle)
    return plot0, plot1, plot2, plot3


# preview a frame
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
data_gen(until_timestep//2)
plt.show()



fig = plt.figure()
#ax = plt.axes(projection='3d')
ax = fig.add_subplot(1, 1, 1, projection='3d')

grav_ani = animation.FuncAnimation(fig, data_gen, frames=np.arange(0, until_timestep, 10),
                              interval=30, blit=False)

#plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg.exe'
Writer = animation.writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Benjamin Oudejans'), bitrate=1800)
filename = 'test.mp4'
print('0%')
begin = time.time()
grav_ani.save(filename, writer=writer)
print('100%')
end = time.time()
print("Animation time:", end-begin, " s")


#
# ax.plot3D(s.y[6], s.y[7], s.y[8], 'gray')
# ax.plot3D([0],[0],[0], marker='o')
# plt.show()
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