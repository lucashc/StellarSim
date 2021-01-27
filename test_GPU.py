from GPU.GPU import GPU
from GPU.types import make_body_array
from time import time
from sys import getsizeof

import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting

cs.set_thread_count(8)


g = GPU()

def genStableGalaxy(n_stars, m_star, m_bh):
    masses = np.array([m_bh] + [m_star]*n_stars)
    r = np.sort(RadDist.radSample(size=n_stars, length_guess=5))
    theta = np.random.uniform(0, 2*np.pi, n_stars)
    positions = np.column_stack((r*np.cos(theta), r*np.sin(theta), np.zeros(n_stars)))
    v_norm = np.sqrt(sc.G*np.cumsum(masses)[:-1]/np.linalg.norm(positions, axis=1))  # skip first cumsum value, since masses includes black hole
    v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
    velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec
    positions = np.insert(positions, 0, np.zeros(3), 0)     # add black hole (already present in masses)
    velocities = np.insert(velocities, 0, -np.sum(velocities*m_star, axis=0)/m_bh, 0)
    print("-----")
    print('\n'.join([str((var, getsizeof(a))) for var, a in locals().items()]))
    # print(velocities)
    # print(velocities*np.expand_dims(masses, axis=0).T)
    # print(np.sum(velocities*np.expand_dims(masses, axis=0).T, axis=0))
    return positions, velocities, masses


thetamax = 0.7
n_steps = 2001
m_star = sc.Msol  # 3.181651515706176e+30
n_star = int(1e5)
pos, vel, mass = genStableGalaxy(n_star, m_star*10, sc.Msgra)

galaxy1 = make_body_array(pos, vel, mass)
galaxy2 = utils.zip_to_bodylist(pos, vel, mass)

del pos, vel, mass


# t1 = time()
# result = g.LeapFrog(galaxy1, dt=1e12, n_steps=n_steps, G=sc.G)
# t2 = time()

# print(f"GPU: {t2-t1} s")

t1 = time()
cs.LeapFrogC(galaxy2, dt=1e12, n_steps=n_steps, G=sc.G, thetamax=0.7)
t2 = time()

print(f"CPU: {t2-t1} s")