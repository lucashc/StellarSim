import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.render as render

thetamax = 0.5
G = 1
n_steps = 100
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
positions = np.concatenate((positions + center1, positions + center2))
velocities = np.concatenate((velocities + v1, velocities + v2))
masses = np.array(masses + masses)

'''
N = 50000

r = 50000
mvar = 10

positions = np.array([np.random.normal(size = N), np.random.normal(size = N), np.zeros(N)]).T * r
masses = 10 + (np.random.normal(size = N)**2)*mvar
total_mass = sum(masses)
transform = np.array([[0, 1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]])
radii = np.linalg.norm(positions, axis=1)
velocities = np.tensordot(positions, transform, axes=1)/radii[..., np.newaxis]
'''
total_bodylist = utils.zip_to_bodylist(positions, velocities, masses)
total_bodylist.check_integrity()
results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps, thetamax, G)
print("done")
s = utils.get_positions(results)
plane = render.Plane(np.array([0, 0, 1]), np.array([0, 0, 0]), np.array([1/8, 0, 0]), np.array([0, 1/8, 0]))
render.animate(s, masses, plane, 400, 400)