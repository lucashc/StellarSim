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