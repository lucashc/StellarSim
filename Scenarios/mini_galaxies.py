import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.plotting as plotting

thetamax = 0.5
G = 1
n_steps = 3000
dt = 3e-2

center1 = np.array([600, 0, 0])
center2 = np.array([-600, 0, 0])
v1 = np.array([-2, 0.6, 0])
v2 = -v1  # equal masses => total momentum 0
m_BH = 100000   # mass of black hole

positions = [np.zeros(3)]
velocities = [np.zeros(3)]
masses = [m_BH]
for r in np.arange(1, 10)*25:      # add stars in rings around black hole
    for theta in np.linspace(0, 2*np.pi, int(3*r/25))[:-1]:
        positions.append(np.array([r*np.sin(theta), r*np.cos(theta), 0]))
        velocities.append(np.array([np.cos(theta), -np.sin(theta), 0])*np.sqrt(G*m_BH/r))
        masses.append(10)

galaxy_bodies = utils.zip_to_bodylist(positions, velocities, masses)
# positions = np.array(positions)
# velocities = np.array(velocities)
N = len(positions)
# all_pos = np.concatenate((positions + center1, positions + center2))
# all_vel = np.concatenate((velocities + v1, velocities + v2))
# all_m = masses + masses
# # galaxy1 = utils.zip_to_bodylist(positions + center1, velocities + v1, masses)
# # galaxy2 = utils.zip_to_bodylist(positions + center2, velocities + v2, masses)
# # all_bodies = galaxy1 + galaxy2
# # N = len(galaxy1)
# # exit()
# # one_body = galaxy1[2]
#
#
# total_bodylist = utils.zip_to_bodylist(all_pos, all_vel, all_m)
axis_begin = np.array([-1, 0, 0])
axis_end = np.array([0, 1, 0])
galaxy1 = utils.rotate_bodylist(galaxy_bodies, np.pi/4, np.array(axis_begin), np.array(axis_end))
galaxy1 = utils.translate_bodylist(galaxy1, center1)
galaxy1 = utils.add_velocity_bodylist(galaxy1, v1)

# points = [axis_begin, axis_end]
# for i in range(len(galaxy1)):
#     body = galaxy1[i]
#     points.append(body.pos)
# points = np.array(points)
#
# fig = plt.figure()
# # ax = plt.axes(projection='3d')
# ax = fig.add_subplot(1, 1, 1, projection='3d')
# ax.set(xlim=(-300, 300))
# ax.plot3D(points[:,0], points[:,1], points[:,2], linestyle="none", marker=".")
# axis_far_end = 200*(axis_end-axis_begin) + axis_begin
# axis_far_begin = -200*(axis_end-axis_begin) + axis_begin
# ax.plot3D(*[[axis_far_begin[i], axis_far_end[i]] for i in range(3)], markersize=10, marker=".")
# plt.show()


galaxy2 = utils.translate_bodylist(galaxy_bodies, center2)
galaxy2 = utils.add_velocity_bodylist(galaxy2, v2)
total_bodylist = utils.concatenate_bodylists(galaxy1, galaxy2)

total_bodylist.check_integrity()
#total_bodylist.save("galaxies.bin")
results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps, thetamax, G)
# for i in range(len(results)):
#     bl = cs.BodyList3(results[i, :])
#     bl.save(f"galaxies{i:3d}.bin")


large_limits = {"xlim": (-1600, 1600), "ylim": (-1600, 1600), "zlim": (-1600, 1600)}
medium_limits = {"xlim": (-1000, 1000), "ylim": (-1000, 1000), "zlim": (-1600, 1000)}
s = utils.get_positions(results)
particles = [4*n for n in range(2*N//4)] + [N]  # 1 in 4 particles + second black hole
particle_config = [{"color": "k", "markersize": "10"}] + (N-1)*[{"color": "b"}] + [{"color": "k", "markersize": "10"}] \
                  + (N-1)*[{"color": "r"}]
plotting.movie3d(s, particles, **medium_limits, mode='point', elevation=20, fps=25, skip_steps=60,
                 particle_config=particle_config, filename="mini_galaxies.mp4")
#plotting.movie3d(s, [0, 2, 30, 60, -1], until_timestep=1000, skip_steps=10, mode="point", **medium_limits)
