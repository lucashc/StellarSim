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

def gen_dummy(pos, DM_pos, m, mDM, mBH):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""
    posarray = pos
    n = len(pos)
    nDM = len(DM_pos)
    massarray = m
    velarray = np.zeros((n, 3))
    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=mBH)]
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


def gen_galaxy(pos, DM_pos, m, mDM, mBH, v, vDM):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""
    posarray = pos
    n = len(pos)
    nDM = len(DM_pos)
    massarray = m
    velarray = v
    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=mBH)]
    for i in range(n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    posarrayDM = DM_pos
    massarrayDM = mDM

    bodiesDM = []
    velarrayDM = vDM
    for i in range(0, nDM):
        bodiesDM.append(cs.Body3(pos=posarrayDM[i], vel=velarrayDM[i], mass=massarrayDM[i], dark_matter=True))
    

    allbodies = np.concatenate((bodies,bodiesDM))

    return cs.BodyList3(np.array(allbodies))



def create_galaxy(n_stars, n_DM_particles, visible_mass, DM_mass, BH_mass, R, R_bulge, R_halo, thetamax=0.7, spherical=True, epsilon=4e16, factor = 0.8, random_DM=True):
    # generate particle masses
    m_stars = md.massSample(n_stars)
    print('mass_ratio =', visible_mass/sum(m_stars))
    m_stars = m_stars * visible_mass/sum(m_stars)
    DM_mass = np.sum(m_stars)*DM_mass/visible_mass
    m_DM = np.ones(n_DM_particles)*DM_mass/n_DM_particles
    
    # generate positions of visible matter
    theta = np.random.uniform(0, 2 * np.pi, n_stars)

    r = np.sort(rd.radSample(size=n_stars, r_char=R/5, r_bulge=R_bulge, rad_min = R_bulge/20))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    if spherical:
        alpha = R_bulge*(0.05+0.4/(1+(r/R_bulge)**2.5))
        z = np.random.uniform(-alpha,alpha, n_stars)
    else:
        z=np.zeros(n_stars)
    posarray = np.column_stack((x, y, z))

    # generate positions of dark matter
    thetaDM = np.random.uniform(0, 2*np.pi, n_DM_particles)
    phiDM = np.arccos(np.random.uniform(-1,1,n_DM_particles))
    rDM = DMrd.PIradSample(n_DM_particles, R_bulge, R_halo)

    xDM = rDM * np.cos(thetaDM) * np.sin(phiDM)
    yDM = rDM * np.sin(thetaDM) * np.sin(phiDM)
    zDM = rDM * np.cos(phiDM)
    posarrayDM = np.column_stack((xDM, yDM, zDM))

    # generate dummy for determining initial velocity norms
    dummy = gen_dummy(posarray, posarrayDM, m_stars, m_DM, BH_mass)
    # result = cs.LeapFrogSaveC(dummy, dt=0, n_steps=1, thetamax=thetamax, G=sc.G, save_every=1, epsilon=epsilon).numpy()
    # g = np.linalg.norm(utils.get_vec_attribute(result, 'g')[0], axis=1)[1:]
    cs.acceleratedAccelerationsC(dummy, thetamax=thetamax, G=sc.G, epsilon=epsilon)
    g = np.linalg.norm([b.g for b in dummy], axis=1)[1:]
    v_norm_vis = np.sqrt(r*g[0:n_stars])
    v_norm_DM = np.sqrt(rDM*g[n_stars:])

    # calculate velocity vector for visible matter 
    v_unit_vec_vis = np.column_stack((-np.sin(theta), np.cos(theta), np.zeros(n_stars)))
    velocities_vis = v_norm_vis.reshape((n_stars, 1)) * v_unit_vec_vis

    # calculate velocity vector for dark matter 
    if random_DM:
        gamma = np.random.uniform(0,2*np.pi,n_DM_particles)
        v_unit_vec_DM = []
        for i, pos in enumerate(posarrayDM):
            b1 = np.array([pos[2],0, -pos[0]])
            b1 /= np.linalg.norm(b1)
            b2 = np.array([0,pos[2], -pos[1]])
            b2 /= np.linalg.norm(b2)
            attenuation_z = (abs(pos[2])/np.linalg.norm(pos))**0.5
            v_unit_vec_DM.append(np.array([1, 1, factor**(1 - attenuation_z)])*(np.cos(gamma[i])*b1 + np.sin(gamma[i])*b2))
    
    else:
        v_unit_vec_DM = np.column_stack((-np.sin(thetaDM), np.cos(thetaDM), np.zeros(n_DM_particles)))

    v_unit_vec_DM = np.array(v_unit_vec_DM)
    velocities_DM = v_norm_DM.reshape((n_DM_particles, 1)) * v_unit_vec_DM
    return gen_galaxy(posarray, posarrayDM, m_stars, m_DM, BH_mass, velocities_vis, velocities_DM)


def create_milky_way(n_stars, n_DM_particles, thetamax=0.7, spherical=True, epsilon=4e16, factor = 0.8, R_halo=3*sc.Rmw, random_DM=True):
    return create_galaxy(n_stars=n_stars, n_DM_particles=n_DM_particles, thetamax=thetamax, visible_mass=sc.Mlummw, DM_mass=sc.MDMmw, BH_mass = sc.Msgra, R=sc.Rmw, R_bulge=sc.RCmw, R_halo = R_halo, spherical=spherical, epsilon=epsilon, factor=factor, random_DM=random_DM)


def create_andromeda(n_stars, n_DM_particles, thetamax=0.7, spherical=True, epsilon=4e16, factor = 0.8, R_halo=3*sc.Randr, random_DM=True):
    return create_galaxy(n_stars=n_stars, n_DM_particles=n_DM_particles, thetamax=thetamax, visible_mass=sc.Mlumandr, DM_mass=sc.MDMandr, BH_mass = sc.Mandrbh, R=sc.Randr, R_bulge=sc.RCandr, R_halo = R_halo, spherical=spherical, epsilon=epsilon, factor = factor, random_DM=random_DM)


if __name__ == '__main__':
    cs.set_thread_count(8)
    MW = create_milky_way(2000, 3000)
    MW.translate(np.array([-1, 0, 0])*sc.ly*1e6/2)
    MW.add_velocity(np.array([1, 0, 0])*225e3/2)
    AM = create_andromeda(2000, 3000)
    AM.rotate(np.pi/6, np.zeros(3, dtype=np.double), np.array([1,1,0], dtype=np.double))
    AM.translate(np.array([1, 0, 0])*sc.ly*1e6/2)
    AM.add_velocity(np.array([-1, 0, 0])*225e3/2)
    Collision = MW + AM
    result = cs.LeapFrogSaveC(Collision, dt=1e13, n_steps=8000, thetamax=0.7, G=sc.G, save_every=10, epsilon=4e16)
    result.save("collision.binv")
