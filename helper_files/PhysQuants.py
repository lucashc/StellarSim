import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs


def mass(result, t=0):
    masses = utils.get_masses(result)[t]
    blackholemass = masses[0]
    return masses, np.sum(masses), blackholemass/np.sum(masses)

def totalMass(masses):
    return np.sum(masses, axis=1)


def linMom(result, t=0):
    masses = np.expand_dims(utils.get_masses(result)[t], axis=0)
    v = utils.get_velocities(result)[t]
    p = v*masses.T
    pmag = np.linalg.norm(p, axis=1)
    sump = np.sum(p, axis=0)
    return p, sump, np.linalg.norm(sump), pmag

def linearMomenta(velocities, masses):
    momenta = velocities*masses
    magnitude = np.linalg.norm(momenta, axis=2)
    summed = np.sum(momenta, axis=1)
    return momenta, summed, np.linalg.norm(summed), np.expand_dims(magnitude, 2)

def angMom(result, t=0):
    r = utils.get_positions(result)[t]
    p = linMom(result, t)[0]
    L = np.cross(r,p)
    sumL = np.sum(L, axis=0)
    return L, sumL, np.linalg.norm(sumL)

def angularMomenta(positions, velocities, masses):
    momenta = velocities*masses
    angular_momenta = np.cross(positions, momenta, axis=2)
    summed = np.sum(angular_momenta, axis=1)
    return angular_momenta, summed, np.linalg.norm(summed)

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


def potential_energies_barnes_hut(result): # return potential energy in each frame
    frames = result.numpy()
    return np.array([cs.getEnergiesC(cs.BodyList3(frame), thetamax=0.7, G=sc.G) for frame in frames])


def energies(positions, velocities, masses, result):
    _, _, _, momenta_magnitudes = linearMomenta(velocities, masses)
    kinetic_energy = np.sum(momenta_magnitudes**2/2/masses, axis = 1)
    potential_energy = np.expand_dims(potential_energies_barnes_hut(result), 1)
    print(potential_energy.shape, kinetic_energy.shape)
    return kinetic_energy+potential_energy, kinetic_energy, potential_energy

def quantities(result):
    positions, velocities, masses = utils.unzip_result(result)
    _, total_momenta, _, magnitude = linearMomenta(velocities, masses)
    _, total_angular_momenta, _ = angularMomenta(positions, velocities, masses)
    #total_energy, _, _ = energies(positions, velocities, masses, result)
    plt.subplot(211)
    plt.plot(np.sum(magnitude, axis = 1), label="Summed absolute momentum")
    plt.plot((total_momenta[:,0]**2 + total_momenta[:,1]**2 + total_momenta[:,2]**2)**0.5, label="Norm of netto momentum")
    plt.title("Plot of the momentum at each timestep")
    plt.xlabel(r"t ($10^{14} s$)")
    plt.ylabel(r"|p| ($kg \cdot m \cdot s^{-1}$)")
    plt.legend()
    plt.subplot(212)
    plt.plot(np.sum(magnitude, axis = 1), label="Summed absolute angular momentum")
    plt.plot((total_angular_momenta[:,0]**2 + total_angular_momenta[:,1]**2 + total_angular_momenta[:,2]**2)**0.5, label="Norm of netto angular momentum")
    plt.title("Plot of the angular momentum at each timestep")
    plt.xlabel(r"t ($10^{14} s$)")
    plt.ylabel(r"|L| ($kg\cdot m^2\cdot s^{-1}$)")
    plt.legend()
    plt.show()



def speedcurve(result, t=0):
    velocities = utils.get_velocities(result)[t]
    positions = utils.get_positions(result)[t]
    plt.plot(np.linalg.norm(positions, axis=1)[1:], np.linalg.norm(velocities, axis=1)[1:], '.')
    plt.xlim(0, sc.Rmw*1.2)
    # plt.ylim(0, 0.1e6)
    plt.xlabel("r (m)")
    plt.ylabel("v (m/s)")
    plt.show()
