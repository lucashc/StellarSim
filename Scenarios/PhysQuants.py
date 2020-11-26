import numpy as np
import matplotlib.pyplot as plt
import Scenarios.stellarConstants as sc
import helper_files.sim_utils as utils

def mass(result,t=0):
    masses = utils.get_masses(result)[t]
    blackholemass = masses[0]
    return masses, sum(masses), blackholemass/sum(masses)

def linMom(result, t=0):
    masses = utils.get_masses(result)[t]
    v = utils.get_velocities(result)[t]
    v_x, v_y, v_z = v[:,0], v[:,1], v[:,2]
    p_x, p_y, p_z = masses * v_x, masses * v_y, masses * v_z
    p = np.column_stack((p_x,p_y,p_z))
    sump = np.array([sum(p_x), sum(p_y), sum(p_z)])
    return p, sump, np.linalg.norm(sump)

def angMom(result, t=0):
    masses = utils.get_masses(result)[t]
    r = utils.get_positions(result)[t]
    p = linMom(result, t)[0]
    L = np.cross(r,p)
    L_x, L_y, L_z = L[:,0], L[:,1], L[:,2]
    sumL = np.array([sum(L_x), sum(L_y), sum(L_z)])
    return L, sumL, np.linalg.norm(sumL)