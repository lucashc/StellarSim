import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.plotting as plotting

thetamax = 0.5
G = 1
n_steps = 1000
dt = 1e-3

center1 = np.array([500, 0, 0])
center2 = np.array([-500, 0, 0])
v1 = np.array([-50, 5, 0])
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

large_limits = {"xlim": (-1000, 1000), "ylim": (-1000, 1000), "zlim": (-1000, 1000)}
total_bodylist = utils.zip_to_bodylist(all_pos, all_vel, all_m)

results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps, thetamax, G)
print("done")
s = utils.get_positions(results)
plotting.movie3d(s, [0,1,N//2,N-1,N,N+1,N+N//2, 2*N-1], mode='line', **large_limits)
