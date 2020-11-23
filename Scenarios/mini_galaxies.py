import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.plotting as plotting

thetamax = 0.5
G = 1
n_steps = 1500
dt = 1e-1

center1 = np.array([400, 0, 0])
center2 = np.array([-400, 0, 0])
v1 = np.array([-3, 0.6, 0])
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

positions = np.array(positions)
velocities = np.array(velocities)
N = len(positions)
all_pos = np.concatenate((positions + center1, positions + center2))
all_vel = np.concatenate((velocities + v1, velocities + v2))
all_m = masses + masses
# galaxy1 = utils.zip_to_bodylist(positions + center1, velocities + v1, masses)
# galaxy2 = utils.zip_to_bodylist(positions + center2, velocities + v2, masses)
# all_bodies = galaxy1 + galaxy2
# N = len(galaxy1)
# exit()
# one_body = galaxy1[2]


total_bodylist = utils.zip_to_bodylist(all_pos, all_vel, all_m)
total_bodylist.check_integrity()
#total_bodylist.save("galaxies.bin")
results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps+1, thetamax, G)
results.save("minigalaxy.binv")
large_limits = {"xlim": (-1600, 1600), "ylim": (-1600, 1600), "zlim": (-1600, 1600)}
s = utils.get_positions(results)
particles = [4*n for n in range(2*N//4)] + [N]  # 1 in 4 particles + second black hole
particle_config = [{"color": "k", "markersize": "10"}] + (N-1)*[{"color": "b"}] + [{"color": "k", "markersize": "10"}] \
                  + (N-1)*[{"color": "r"}]
plotting.movie3d(s, particles, **large_limits, mode='point', elevation=20, fps=25, skip_steps=20,
                 particle_config=particle_config)
#plotting.movie3d(s, [0, 2, 30, 60, -1], until_timestep=1000, skip_steps=10, mode="point", **medium_limits)
