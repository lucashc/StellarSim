import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting
from copy import copy


def genStableGalaxy(n_stars, m_star, m_bh):
    masses = np.array([m_bh] + [m_star]*n_stars)
    r = np.sort(RadDist.radSample(size=n_stars))
    theta = np.random.uniform(0, 2*np.pi, n_stars)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = np.zeros(n_stars)
    positions = np.column_stack((x, y, z))
    v_norm = np.sqrt(sc.G*np.cumsum(masses)[:-1]/np.linalg.norm(positions, axis=1))  # skip first cumsum value, since masses includes black hole
    v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
    velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec
    positions = np.insert(positions, 0, np.zeros(3), 0)     # add black hole (already present in masses)
    velocities = np.insert(velocities, 0, -np.sum(velocities*m_star, axis=0)/m_bh, 0)
    print(velocities)
    print(velocities*np.expand_dims(masses, axis=0).T)
    print(np.sum(velocities*np.expand_dims(masses, axis=0).T, axis=0))
    return utils.zip_to_bodylist(positions, velocities, masses)


thetamax = 0.7
n_steps = 5000
m_star = sc.Msol  # 3.181651515706176e+30
galaxy1 = genStableGalaxy(10000, m_star, sc.Msgra)
galaxy2 = copy(galaxy1)

# Galaxy 1
print("Galaxy 1")
eps = 0.0
result = cs.LeapFrogSaveC(galaxy1, 1e12, n_steps, thetamax, sc.G, 10, eps)
result.save("stable_test.binv")

# Galaxy 2
print("Galaxy 2")
eps = 15e13
result = cs.LeapFrogSaveC(galaxy2, 1e12, n_steps, thetamax, sc.G, 10, eps)
result.save("stable_test_with_eps.binv")
# result = cs.Result.load("stable2.binv").numpy()
# print(result.shape)
# plotting.movie3d(result, [0], skip_steps=10)
