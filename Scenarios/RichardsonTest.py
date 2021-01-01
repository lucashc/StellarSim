import helper_files.RichardsonError as RE
import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting
import matplotlib.pyplot as plt
import copy

cs.set_thread_count(8)
np.random.seed(2147483648)

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


thetamax = 0.0
n_steps = 1
m_star = sc.Msol  # 3.181651515706176e+30
galaxy = genStableGalaxy(10000, m_star*10, sc.Msgra)
galaxy.check_integrity()
pos_p, vel_p = RE.richardson_error(galaxy, 1e11, sc.G, n_steps=n_steps)
print(np.nanmean(pos_p), np.nanmean(vel_p))
ax1 = plt.subplot(211)
bins = np.arange(-3, 5, 0.25)
plt.hist(pos_p, histtype='bar', ec='black', bins=bins)
plt.ylabel("Frequency")
plt.xlabel("Order $p$")
plt.title("Orders of $\mathbf{x}_i$")
ax2 = plt.subplot(212, sharex=ax1)
plt.hist(vel_p, histtype='bar', ec='black', bins=bins)
plt.xlabel("Order $p$")
plt.ylabel("Frequency")
plt.title("Orders of $\mathbf{v}_i$")
plt.xlim(-2, 5)
plt.tight_layout()
plt.show()