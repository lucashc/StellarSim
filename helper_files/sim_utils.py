import cppsim as cs
import numpy as np


def make_body(pos, vel, m):
    """A more flexible wrapper for the Body3 constructor. Accepts native python objects
     such as lists and floats, as well as numpy objects"""
    return cs.Body3(np.array(pos, dtype=np.double), np.array(vel, dtype=np.double), np.double(m))


def zip_to_bodylist(pos_list, vel_list, m_list):
    """Constructs a BodyList3 from iterables of positions, velocities and masses.
     Accepts native python & numpy objects"""
    bodies = [make_body(pos, vel, m) for pos, vel, m in zip(pos_list, vel_list, m_list)]
    return cs.BodyList3(np.array(bodies))


def get_vec_attribute(result, attr):
    """Get a vector attribute from bodies from C++ simulation """
    n_steps = len(result)
    N = len(result[0])
    s = np.empty((n_steps, N, 3))
    for i in range(n_steps):
        for j in range(N):
            s[i, j, :] = getattr(result[i, j], attr)

    return s

def get_sca_attribute(result, attr):
    """Get scalar attribute from bodies from C++ simulation """
    n_steps = len(result)
    N = len(result[0])
    s = np.empty((n_steps, N))
    for i in range(n_steps):
        for j in range(N):
            s[i, j] = getattr(result[i, j], attr)

    return s

def get_positions(result):
    """Get positions from bodies from C++ simulation """
    return get_vec_attribute(result.numpy(), 'pos')


def get_velocities(result):
    """Get velocities from bodies from C++ simulation """
    return get_vec_attribute(result.numpy(), 'vel')

def get_masses(result):
    """Get velocities from bodies from C++ simulation """
    return get_sca_attribute(result.numpy(), 'mass')
