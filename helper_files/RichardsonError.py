import numpy as np
import barneshut_cpp.cppsim as cs
import helper_files.sim_utils as utils
import copy

def richardson_fraction(h1, h2, h4):
    print(h1 -h2, h2 - h4)
    print((h2 - h4)/(h1 - h2))
    return (h2 - h4)/(h1 - h2)

def richardson_error(body_list, h, G, thetamax = 0, n_steps = 1, epsilon = 0, DM_mass=0):
    h1_bodies = copy.copy(body_list)
    h2_bodies = copy.copy(body_list)
    h4_bodies = copy.copy(body_list)
    cs.ModifiedEulerC(h1_bodies, h, 4*n_steps, thetamax, G, epsilon, DM_mass)
    cs.ModifiedEulerC(h2_bodies, 2*h, 2*n_steps, thetamax, G, epsilon, DM_mass)
    cs.ModifiedEulerC(h4_bodies, 4*h, n_steps, thetamax, G, epsilon, DM_mass)
    pos_h1, vel_h1, _ = utils.unzip_bodylist(h1_bodies)
    pos_h2, vel_h2, _ = utils.unzip_bodylist(h2_bodies)
    pos_h4, vel_h4, _ = utils.unzip_bodylist(h4_bodies)
    pos_h1 = pos_h1[:, 0:1].flatten()
    vel_h1 = vel_h1[:, 0:1].flatten()
    pos_h2 = pos_h2[:, 0:1].flatten()
    vel_h2 = vel_h2[:, 0:1].flatten()
    pos_h4 = pos_h4[:, 0:1].flatten()
    vel_h4 = vel_h4[:, 0:1].flatten()
    return np.log2(richardson_fraction(pos_h1, pos_h2, pos_h4)), np.log2(richardson_fraction(vel_h1, vel_h2, vel_h4))
