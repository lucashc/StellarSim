import cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation



until_timestep = 1000
r0 = np.array([[0, 0, 0], [50, 0, 0], [0, 50, 0], [-100, -100, 0]], dtype=np.double)
v0 = np.array([[0, 0, 0], [0, 100, 50], [-100, 0, 20], [-10, -30, 0]], dtype=np.double)
m = np.array([1e6, 1, 10000, 10], dtype=np.double)
N = len(r0)

# N = 2
# until_timestep = int(1e5)
# r0 = np.array([[-50, 0, 0], [50, 0, 0]], dtype=np.double)
# v0 = np.array([[0, -0.7, 0], [0, 0.7, 0]], dtype=np.double)
# m = np.array([100, 100], dtype=np.double)

bodies = np.array([cs.Body3(r0[i], v0[i], m[i]) for i in range(N)])
bodylist = cs.BodyList3(bodies)

result = cs.EulerForwardSaveC(bodylist, 1e-2, until_timestep, 0, 1)

s = np.empty((until_timestep, N, 3))
for i in range(until_timestep):
    for j in range(N):
        s[i, j, :] = result[i, j].pos


large_limits = {"xlim": (-1000, 1000), "ylim": (-1000, 1000), "zlim":(-1000, 1000)}
sun_limits = {"xlim": (-20, 1), "ylim": (-10, 10), "zlim": (-1, 5)}
starting_angle = 270  # default 270, 0 for sun zoom
rotation_speed = 40  # default 40
elevation = 10  # default 0

def data_gen(index):
    ax.clear()
    #ax.axis('off')
    ax.grid('off')
    plot0 = ax.plot3D(s[:index, 0, 0], s[:index, 0, 1], s[:index, 0, 2], linewidth=1)
    plot1 = ax.plot3D(s[:index, 1, 0], s[:index, 1, 1], s[:index, 1, 2],)
    plot2 = ax.plot3D(s[:index, 2, 0], s[:index, 2, 1], s[:index, 2, 2])
    plot3 = ax.plot3D(s[:index, 3, 0], s[:index, 3, 1], s[:index, 3, 2])
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

Writer = animation.writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Lucas Crijns'), bitrate=1800)
filename = 'test.mp4'
print('0%')
# begin = time.time()
grav_ani.save(filename, writer=writer)
print('100%')
# end = time.time()
# print("Animation time:", end-begin, " s")