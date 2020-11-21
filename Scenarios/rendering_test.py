import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.render as render

thetamax = 0.5
G = 1
n_steps = 10
dt = 1e-1

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

total_bodylist = utils.zip_to_bodylist(positions, velocities, masses)
total_bodylist.check_integrity()
results = cs.LeapFrogSaveC(total_bodylist, dt, n_steps, thetamax, G)
print("done")
s = utils.get_positions(results)
plane = render.Plane(np.array([0, 0, 1]), np.array([0, 0, 0]), np.array([1/1600, 0, 0]), np.array([0, 1/1600, 0]))
render.animate(s, masses, plane, 400, 400)