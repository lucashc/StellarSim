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

N = len(positions)

galaxy_bodies = utils.zip_to_bodylist(positions, velocities, masses)
galaxy1 = utils.rotate_bodylist(galaxy_bodies, np.pi/4, np.array([-1, 0, 0]), np.array([0, 1, 0]))
galaxy1 = utils.translate_bodylist(galaxy1, center1)
galaxy1 = utils.add_velocity_bodylist(galaxy1, v1)

galaxy2 = utils.translate_bodylist(galaxy_bodies, center2)
galaxy2 = utils.add_velocity_bodylist(galaxy2, v2)

total_bodylist = utils.concatenate_bodylists(galaxy1, galaxy2)
total_bodylist.check_integrity()
#total_bodylist.save("galaxies.bin")
results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps, thetamax, G)
# for i in range(len(results)):
#     bl = cs.BodyList3(results[i, :])
#     bl.save(f"galaxies{i:3d}.bin")
# exit()
large_limits = {"xlim": (-1600, 1600), "ylim": (-1600, 1600), "zlim": (-1600, 1600)}
s = utils.get_positions(results)
particles = [4*n for n in range(2*N//4)] + [N]  # 1 in 4 particles + second black hole
particle_config = [{"color": "k", "markersize": "10"}] + (N-1)*[{"color": "b"}] + [{"color": "k", "markersize": "10"}] \
                  + (N-1)*[{"color": "r"}]
plotting.movie3d(s, particles, **large_limits, mode='point', elevation=20, fps=25, skip_steps=20,
                 particle_config=particle_config)
#plotting.movie3d(s, [0, 2, 30, 60, -1], until_timestep=1000, skip_steps=10, mode="point", **medium_limits)
