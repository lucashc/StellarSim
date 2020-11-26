import Scenarios.RadDist as RadDist
import Scenarios.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs

def genStableGalaxy(n_stars, m_star, m_bh):
    masses = np.array([m_bh] + [m_star]*n_stars)
    r = np.sort(RadDist.radSample(size=n_stars))
    theta = np.random.uniform(0, 2*np.pi, n_stars)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = np.zeros(n_stars)
    positions = np.column_stack((x, y, z))

    v_norm = np.sqrt(sc.G*np.cumsum(masses)[1:]/np.linalg.norm(positions))  # skip first cumsum value, since masses includes black hole
    v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
    velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec
    positions = np.insert(positions, 0, np.zeros(3), 0)     # add black hole (already present in masses)
    velocities = np.insert(velocities, 0, np.zeros(3), 0)
    return utils.zip_to_bodylist(positions, velocities, masses)


thetamax = 0.7
n_steps = 1000
galaxy = genStableGalaxy(1000, 10, 1000)
result = cs.LeapFrogSaveC(galaxy, 1e12, n_steps, thetamax, sc.G)
result.save("stable.binv")
