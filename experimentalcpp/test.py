import cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


N = 4
r0 = np.array([[0, 0, 0], [50, 0, 0], [0, 50, 0], [-100, -100, 0]], dtype=np.double)
v0 = np.array([[0, 0, 0], [0, 100, 50], [-100, 0, 20], [-10, -30, 0]], dtype=np.double)
m = np.array([1e6, 1, 10000, 10], dtype=np.double)
bodies = np.array([cs.Body3(r0[i], v0[i], m[i]) for i in range(N)])
bodylist = cs.BodyList3(bodies)


result = cs.EulerForwardSaveC(bodylist, 10, 100, 0.5, 1)

exit()

until_timestep = 100
large_limits = {"xlim": (-140, 70), "ylim": (-120, 60), "zlim":(-15, 15)}
sun_limits = {"xlim": (-20, 1), "ylim": (-10, 10), "zlim": (-1, 5)}
starting_angle = 0  # default 270, 0 for sun zoom
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
    ax.set(**sun_limits)
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

plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg.exe'
Writer = animation.writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Benjamin Oudejans'), bitrate=1800)
filename = 'C:/Users/benja/Pictures/MathViz/grav_ani_sunzoom.mp4'
print('0%')
# begin = time.time()
grav_ani.save(filename, writer=writer)
print('100%')
# end = time.time()
# print("Animation time:", end-begin, " s")