import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import helper_files.sim_utils as utils


def mass(result,t=0):
    masses = utils.get_masses(result)[t]
    blackholemass = masses[0]
    return masses, np.sum(masses), blackholemass/np.sum(masses)


def linMom(result, t=0):
    masses = np.expand_dims(utils.get_masses(result)[t], axis=0)
    v = utils.get_velocities(result)[t]
    p = v*masses.T
    pmag = np.linalg.norm(p, axis=1)
    sump = np.sum(p, axis=0)
    return p, sump, np.linalg.norm(sump), pmag


def angMom(result, t=0):
    r = utils.get_positions(result)[t]
    p = linMom(result, t)[0]
    L = np.cross(r,p)
    sumL = np.sum(L, axis=0)
    return L, sumL, np.linalg.norm(sumL)


def energy(result,t=0):
    masses = utils.get_masses(result)[t]
    r = utils.get_positions(result)[t]
    pmag = linMom(result,t)[3]
    Ekin = np.sum(pmag**2/(2*masses))
    Epot = 0
    for i in range(len(masses)):
        for j in range(i+1,len(masses)):
            dist = np.linalg.norm(r[i]-r[j])
            Epot -= sc.G*masses[i]*masses[j]/dist

    return Ekin+Epot, Ekin, Epot


def speedcurve(result, t=0):
    velocities = utils.get_velocities(result)[t]
    positions = utils.get_positions(result)[t]
    plt.plot(np.linalg.norm(positions, axis=1)[1:], np.linalg.norm(velocities, axis=1)[1:], '.')
    plt.xlim(0, 0.25e20)
    plt.ylim(0, 0.1e6)
    plt.xlabel("r (m)")
    plt.ylabel("v (m/s)")
    plt.show()
