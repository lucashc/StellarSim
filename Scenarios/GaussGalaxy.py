import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting

cs.set_thread_count(8)

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
    # print(velocities)
    # print(velocities*np.expand_dims(masses, axis=0).T)
    # print(np.sum(velocities*np.expand_dims(masses, axis=0).T, axis=0))
    return utils.zip_to_bodylist(positions, velocities, masses)


thetamax = 0.7
n_steps = 2000
m_star = sc.Msol  # 3.181651515706176e+30
galaxy = genStableGalaxy(int(1e5), m_star*10, sc.Msgra)
M = 5000*m_star*10 + sc.Msgra
# cs.LeapFrogC(galaxy, 1e12, 5000, thetamax, sc.G)
print("Done with step 1")
result = cs.LeapFrogSaveC(galaxy, dt=1e12, n_steps=n_steps, thetamax=thetamax, G=sc.G, save_every=10, epsilon=15e13, DM_mass=0)
result.save("stable_test.binv")

# result = cs.Result.load("stable2.binv").numpy()
# print(result.shape)
# plotting.movie3d(result, [0], skip_steps=10)
