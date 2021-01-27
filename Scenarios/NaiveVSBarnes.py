from GPU.GPU import GPU
from GPU.types import make_body_array
from time import time
from sys import stderr
import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting


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
    return positions, velocities, masses

# Global parameters
cs.set_thread_count(8)
g = GPU()
thetamax = 0.7
n_steps = 10
m_star = sc.Msol  # 3.181651515706176e+30
n_star = np.linspace(1, int(1e5), 30, dtype=np.int)


def run_CPU(galaxy):
    galaxy_b = utils.zip_to_bodylist(*galaxy)
    t1 = time()
    cs.LeapFrogC(galaxy_b, dt=1e12, n_steps=n_steps, G=sc.G, thetamax=0.7)
    t2 = time()
    return t2-t1

def run_GPU(galaxy):
    galaxy_a = make_body_array(*galaxy)
    t1 = time()
    result = g.LeapFrog(galaxy_a, dt=1e12, n_steps=n_steps, G=sc.G)
    t2 = time()
    return t2-t1

# Benchmark

output = open('algorithm_comparison.csv', 'w')

print("Count;CPU;GPU", file=output, flush=True)
for index, n in enumerate(n_star):
    print(f"At iteration {index+1} of {len(n_star)}, experimenting with {n} particles")
    galaxy = genStableGalaxy(n, m_star*10, sc.Msgra)
    t1 = run_CPU(galaxy)
    t2 = run_GPU(galaxy)
    print(f"{n};{t1};{t2}", file=output, flush=True)
    del galaxy
output.close()