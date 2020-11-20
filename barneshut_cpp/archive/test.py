import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.plotting as plotting

G = 1
thetamax = 0.5

# ---circles around mutual COM (for testing)---
# N = 2
# n_steps = int(1e5)
# r0 = [[-50, 0, 0], [50, 0, 0]]
# v0 = [[0, -np.sqrt(2)/2, 0], [0, np.sqrt(2), 0]]
# m = [100, 100]
# bodies = np.array([cs.Body3(r0[i], v0[i], m[i]) for i in range(N)])
# bodylist = cs.BodyList3(bodies)


# ---original starting conditions---
# r0 = np.array([[0, 0, 0], [50, 0, 0], [0, 50, 0], [-100, -100, 0]], dtype=np.double)
# v0 = np.array([[0, 0, 0], [0, 100, 50], [-100, 0, 20], [-10, -30, 0]], dtype=np.double)
# m = np.array([1e6, 1, 10000, 10], dtype=np.double)
# bodylist = utils.zip_to_bodylist(r0, v0, m)
# N = len(bodylist)


# ---mini-galaxy: bodies arranged in rings around a black hole---
m_BH = 100000   # mass of black hole
galaxy_bodies = [utils.make_body(np.zeros(3), np.zeros(3), m_BH)]  # black hole
for r in np.arange(1, 10)*25:      # add stars
    for theta in np.linspace(0, 2*np.pi, int(3*r/25))[:-1]:
        pos = np.array([r*np.sin(theta), r*np.cos(theta), 0], dtype=np.double)
        v = np.array([np.cos(theta), -np.sin(theta), 0], dtype=np.double)*np.sqrt(G*m_BH/r)
        m = np.double(10)
        galaxy_bodies.append(cs.Body3(pos, v, m))


bodylist = cs.BodyList3(np.array(galaxy_bodies))
n_steps = 30000  # int(30/1e-4)
begin = time.time()
result = cs.LeapFrogSaveC(bodylist, 1e-2, n_steps, thetamax, G)
end = time.time()
print("Simulation finished after", end-begin, "s")

s = utils.get_positions(result)

large_limits = {"xlim": (-1000, 1000), "ylim": (-1000, 1000), "zlim": (-1000, 1000)}
medium_limits = {"xlim": (-300, 300), "ylim": (-300, 300), "zlim": (-300, 300)}
plotting.movie3d(s, [0, 2, 30, 60, -1], until_timestep=1000, skip_steps=10, mode="point", **medium_limits)

