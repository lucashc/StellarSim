import helper_files.RadDist as RadDist
import helper_files.stellarConstants as sc
import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
import helper_files.plotting as plotting
import helper_files.PhysQuants as PQ
import matplotlib.pyplot as plt
import helper_files.MassDist as MassDist

a_0 = 1.2e-10

np.random.seed(1)


def genDMGalaxy(n_stars, m_stars, m_bh, DM_mass):
    # masses = np.array([m_bh] + [m_star]*n_stars)
    # masses = np.array([m_star]*n_stars)
    masses = np.insert(m_stars, 0, m_bh)
    r = np.sort(RadDist.radSample(size=n_stars))
    theta = np.random.uniform(0, 2*np.pi, n_stars)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = np.zeros(n_stars)
    positions = np.column_stack((x, y, z))
    r_max = r[-1]

    norm_const = r_max / sc.RCmw - np.arctan(r_max / sc.RCmw)
    v_norm = 3*np.sqrt(sc.G*np.cumsum(masses)[:-1]/r + sc.G*DM_mass/r * (r/sc.RCmw - np.arctan(r/sc.RCmw))/norm_const)
    print('v_avg', np.sum(v_norm)/len(v_norm))
    # plt.plot([sc.RCmw, sc.RCmw], [0, 1e2])
    plt.plot(r, v_norm)
    # plt.xlim(0, 2.4e19)
    # plt.ylim(0, 3e4)
    # plt.show()
    v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
    velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec
    positions = np.insert(positions, 0, np.zeros(3), 0)     # add black hole (already present in masses)
    momentum = velocities*np.expand_dims(m_stars, axis=1)
    velocities = np.insert(velocities, 0, np.zeros(3), 0)  # -np.sum(momentum, axis=0)/m_bh, 0)
    return utils.zip_to_bodylist(positions, velocities, masses), r, v_norm


thetamax = 0.7
n_steps = 5000
n_stars = 10000
# m_star = sc.Msol  # 3.181651515706176e+30
m_stars = MassDist.massSample(n_stars)
print(sum(m_stars)/len(m_stars))
m_BH = sc.Msgra  # / 1e4
mass_ratio = (sc.Mlummw - m_BH)/sum(m_stars)
print(mass_ratio)
m_stars = mass_ratio*m_stars
m_DM = (np.sum(m_stars) + m_BH)*5
galaxy, r_, vnorm = genDMGalaxy(10000, m_stars, m_BH, m_DM)

result = cs.LeapFrogSaveC(galaxy, dt=1e12, n_steps=1, thetamax=thetamax, G=sc.G, save_every=1, epsilon=4e18,
                          DM_mass=m_DM).numpy()

r = utils.get_positions(result)
r = np.linalg.norm(r[0], axis=1)
g = utils.get_vec_attribute(result, 'g')
plt.subplot(1,2,1)
plt.plot(r, np.linalg.norm(g[0], axis=1))
plt.subplot(1,2,2)
plt.plot(r, np.sqrt(r*np.linalg.norm(g[0], axis=1)), label='model')
plt.plot(r_, vnorm, label='theory')
plt.legend()
plt.show()
exit()

print("Done with step 1")
result = cs.LeapFrogSaveC(galaxy, dt=1e12, n_steps=n_steps, thetamax=thetamax, G=sc.G, save_every=10, epsilon=4e18,
                          DM_mass=m_DM)
result.save("PI_test.binv")
print("Done saving")
PQ.speedcurve(result.numpy(), -1)

# result = cs.Result.load("stable2.binv").numpy()
# print(result.shape)
# plotting.movie3d(result, [0], skip_steps=10)
