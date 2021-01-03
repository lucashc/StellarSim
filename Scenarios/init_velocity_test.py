import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting
import helper_files.PhysQuants as PQ
import matplotlib.pyplot as plt
import helper_files.MassDist as MassDist
import matplotlib as mpl





np.random.seed(1)


def gen_dummy(r, theta, m, m_bh):
    n_stars = len(r)
    masses = np.insert(m, 0, m_bh)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros(n_stars)
    positions = np.column_stack((x, y, z))
    velocities = np.zeros((n_stars, 3))
    positions = np.insert(positions, 0, np.zeros(3), 0)
    velocities = np.insert(velocities, 0, np.zeros(3), 0)
    return utils.zip_to_bodylist(positions, velocities, masses)


def gen_galaxy(r, theta, v, m, m_bh):
    n_stars = len(r)
    masses = np.insert(m, 0, m_bh)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros(n_stars)
    positions = np.column_stack((x, y, z))
    velocities = v
    positions = np.insert(positions, 0, np.zeros(3), 0)
    velocities = np.insert(velocities, 0, np.zeros(3), 0)
    return utils.zip_to_bodylist(positions, velocities, masses)


thetamax = 0.7
n_steps = 5000
n_stars = 10000
theta = np.random.uniform(0, 2 * np.pi, n_stars)
r = np.sort(RadDist.radSample(size=n_stars))
m_stars = MassDist.massSample(n_stars)
m_BH = sc.Msgra
mass_ratio = (sc.Mlummw - m_BH)/sum(m_stars)
# m_stars = mass_ratio*m_stars
m_BH /= mass_ratio
m_DM = (np.sum(m_stars) + m_BH)*5
#plt.scatter(r, m_stars)
#plt.show()

dummy = gen_dummy(r, theta, m_stars, m_BH)
# cs.acceleratedAccelerationsC(dummy)
# g = np.array([body.g for body in dummy])
result = cs.LeapFrogSaveC(dummy, dt=0, n_steps=1, thetamax=thetamax, G=sc.G, save_every=1, epsilon=4e18,
                          DM_mass=m_DM).numpy()
g = np.linalg.norm(utils.get_vec_attribute(result, 'g')[0], axis=1)
v_norm = np.sqrt(r*g[1:])

r_max = sc.Rmw # r[-1]
norm_const = r_max / sc.RCmw - np.arctan(r_max / sc.RCmw)
g_DM = sc.G*m_DM/r**2 * (r/sc.RCmw - np.arctan(r/sc.RCmw))/norm_const

plt.subplot(2, 1, 1)
plt.plot(r, v_norm)
plt.subplot(2, 1, 2)
plt.plot(r, g[1:], label='model')
plt.plot(r, g_DM, label='Pseudo-Iso')
plt.legend()
plt.show()
v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec

galaxy = gen_galaxy(r, theta, velocities, m_stars, m_BH)
print("Done with step 1")
result = cs.LeapFrogSaveC(galaxy, dt=1e12, n_steps=n_steps, thetamax=thetamax, G=sc.G, save_every=10, epsilon=4e18,
                          DM_mass=m_DM)
result.save("IV_test.binv")
print("Done saving")
PQ.speedcurve(result.numpy(), -1)
