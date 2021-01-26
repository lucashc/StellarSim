import numpy as np
from matplotlib import pyplot as plt
import barneshut_cpp.cppsim as cs
import time
import helper_files.sim_utils as utils
import helper_files.plotting as plotting
import helper_files.stellarConstants as sc
import helper_files.RadDist as rd
import helper_files.MassDist as md
import helper_files.DMRadDistNew as DMrd
import helper_files.PhysQuants as pq
from mpl_toolkits import mplot3d

def gen_dummy(pos, DM_pos, m, mDM):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""
    posarray = pos
    n = len(pos)
    nDM = len(DM_pos)
    massarray = m
    velarray = np.zeros((n, 3))
    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=sc.Msgra/1e6)]
    for i in range(n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    posarrayDM = DM_pos
    massarrayDM = mDM

    bodiesDM = []
    velarrayDM = np.zeros((nDM, 3))
    for i in range(0, nDM):
        bodiesDM.append(cs.Body3(pos=posarrayDM[i], vel=velarrayDM[i], mass=massarrayDM[i], dark_matter=True))
    

    allbodies = np.concatenate((bodies,bodiesDM))
    print(len(allbodies))

    return cs.BodyList3(np.array(allbodies))


def gen_galaxy(pos, DM_pos, m, mDM, v, vDM):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""
    posarray = pos
    n = len(pos)
    nDM = len(DM_pos)
    massarray = m
    velarray = v
    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=sc.Msgra/1e6)]
    for i in range(n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    posarrayDM = DM_pos
    massarrayDM = mDM

    bodiesDM = []
    velarrayDM = vDM
    for i in range(0, nDM):
        bodiesDM.append(cs.Body3(pos=posarrayDM[i], vel=velarrayDM[i], mass=massarrayDM[i], dark_matter=True))
    

    allbodies = np.concatenate((bodies,bodiesDM))
    print(len(allbodies))

    return cs.BodyList3(np.array(allbodies))


print('start')
thetamax = 0.7
n_steps = 5000
n_stars = 3000
n_DM_particles = 3000

m_stars = md.massSample(n_stars)
DM_mass = np.sum(m_stars)*5
m_DM = np.ones(n_DM_particles)*DM_mass/n_DM_particles
spherical = True

theta = np.random.uniform(0, 2 * np.pi, n_stars)
if spherical == True:
    phi = np.pi/2 - np.random.normal(0,0.1,n_stars)
else:
    phi = np.pi/2

r = np.sort(rd.radSample(size=n_stars))
x = r * np.cos(theta) * np.sin(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(phi)
posarray = np.column_stack((x, y, z))


print('1')



thetaDM = np.random.uniform(0,2*np.pi,n_DM_particles)
phiDM = np.arccos(2*np.random.uniform(0,1,n_DM_particles)-1)
rDM = DMrd.PIradSample(n_DM_particles, R_halo=18)

xDM = rDM * np.cos(thetaDM) * np.sin(phiDM)
yDM = rDM * np.sin(thetaDM) * np.sin(phiDM)
zDM = rDM * np.cos(phiDM)
posarrayDM = np.column_stack((xDM, yDM, zDM))

print('2')

dummy = gen_dummy(posarray, posarrayDM, m_stars, m_DM)
result = cs.LeapFrogSaveC(dummy, dt=0, n_steps=1, thetamax=thetamax, G=sc.G, save_every=1, epsilon=4e18).numpy()
g = np.linalg.norm(utils.get_vec_attribute(result, 'g')[0], axis=1)[1:]
print(len(g))
v_norm = np.sqrt(r*g[0:n_stars])
v_norm_DM = np.sqrt(rDM*g[n_stars:])
plt.subplot(121)
plt.hist(v_norm)
plt.subplot(122)
plt.hist(v_norm_DM)
plt.show()
v_unit_vec = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
velocities = v_norm.reshape((n_stars, 1)) * v_unit_vec



gamma = np.random.uniform(0,2*np.pi,n_DM_particles)
v_unit_vec_DM = []
for i, pos in enumerate(posarrayDM):
    b1 = np.array([pos[2],0, -pos[0]])
    b1 /= np.linalg.norm(b1)
    b2 = np.array([0,pos[2], -pos[1]])
    b2 /= np.linalg.norm(b2)
    v_unit_vec_DM.append(np.cos(gamma[i])*b1 + np.sin(gamma[i])*b2)

v_unit_vec_DM = np.array(v_unit_vec_DM)
velocities_DM = v_norm_DM.reshape((n_DM_particles, 1)) * v_unit_vec_DM

plt.subplot(121)
plt.hist(np.linalg.norm(velocities, axis = 1))
plt.subplot(122)
plt.hist(np.linalg.norm(velocities, axis =1))

galaxy = gen_galaxy(posarray, posarrayDM, m_stars, m_DM, velocities, velocities_DM)
print("Done with step 1")
result = cs.LeapFrogSaveC(galaxy, dt=5e15, n_steps=n_steps, thetamax=thetamax, G=sc.G, save_every=10, epsilon=4e16)
result.save("bolletjes_test.binv")
print("Done saving")
#PQ.speedcurve(result.numpy(), -1)