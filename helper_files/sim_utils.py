import barneshut_cpp.cppsim as cs
import numpy as np


def make_body(pos, vel, m, dark_matter=False):
    """A more flexible wrapper for the Body3 constructor. Accepts native python objects
     such as lists and floats, as well as numpy objects"""
    return cs.Body3(np.array(pos, dtype=np.double), np.array(vel, dtype=np.double), np.double(m), dark_matter=dark_matter)


def zip_to_bodylist(pos_list, vel_list, m_list, dark_matter_list = None):
    """Constructs a BodyList3 from iterables of positions, velocities and masses.
     Accepts native python & numpy objects"""
    if dark_matter_list is None:
        dark_matter_list = np.full(len(pos_list), False)
    bodies = [make_body(pos, vel, m, dark_matter=dm) for pos, vel, m, dm in zip(pos_list, vel_list, m_list, dark_matter_list)]
    return cs.BodyList3(np.array(bodies))


def unzip_bodylist(bodylist, dark_matter=False):
    """Returns the positions, velocities and masses of the bodies in the bodylist as separate numpy arrays.
    Usage: pos, vel, m = unzip_bodylist(bodylist)"""
    N = len(bodylist)
    positions = np.zeros((N, 3), dtype=np.double)
    velocities = np.zeros((N, 3), dtype=np.double)
    masses = np.zeros(N, dtype=np.double)
    dark_matter_list = np.full(N, False)
    for i in range(len(bodylist)):
        body = bodylist[i]
        positions[i] = body.pos
        velocities[i] = body.vel
        masses[i] = body.mass
        dark_matter_list[i] = body.dark_matter

    if dark_matter:
        return positions, velocities, masses, dark_matter_list
    else:
        return positions, velocities, masses

def unzip_result(result):
    data = result.numpy()
    positions, velocities, masses =  list(map(np.array, zip(*[unzip_bodylist(item) for item in data]))) # (positions, velocities, masses) timestep  particle 
    return positions, velocities, np.expand_dims(masses, axis = 2)

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
    """Get positions from bodies from C++ simulation"""
    return get_vec_attribute(result, 'pos')


def get_velocities(result):
    """Get velocities from bodies from C++ simulation"""
    return get_vec_attribute(result, 'vel')


def get_masses(result): 
    """Get velocities from bodies from C++ simulation"""
    return get_sca_attribute(result, 'mass')


def rotate_bodylist(bodylist, angle, axis_begin, axis_end):
    """Rotate all points in a bodylist around the axis. axis_begin and axis_end determine the axis around which the
    bodies will be rotated, the angle (in radians) determines by how much. Velocities are automatically adjusted too."""
    axis = axis_end - axis_begin
    k = axis/np.linalg.norm(axis)

    def rotate_vector(vector, angle, center, k):
        v = vector - center
        v_rot = v*np.cos(angle) + np.cross(k, v)*np.sin(angle) + k*np.dot(v, k).reshape((len(v), 1))*(1-np.cos(angle))
        return v_rot + center

    positions, velocities, masses, dark_matter_list = unzip_bodylist(bodylist, dark_matter=True)
    new_positions = rotate_vector(positions, angle, axis_begin, k)
    new_velocities = rotate_vector(velocities, angle, axis_begin, k)
    return zip_to_bodylist(new_positions, new_velocities, masses, dark_matter_list )


def translate_bodylist(bodylist, translation):
    """Translate all bodies by the translation vector"""
    positions, velocities, masses, dark_matter_list = unzip_bodylist(bodylist, dark_matter=True)
    new_positions = positions + translation
    return zip_to_bodylist(new_positions, velocities, masses, dark_matter_list)


def add_velocity_bodylist(bodylist, vel):
    """Add constant velocity vel to each body"""
    positions, velocities, masses, dark_matter_list = unzip_bodylist(bodylist, dark_matter=True)
    new_velocities = velocities + vel
    return zip_to_bodylist(positions, new_velocities, masses, dark_matter_list)


def concatenate_bodylists(*bodylists):
    """Concatenates bodylists together. Accepts any amount of bodylists as arguments"""
    positions = np.empty((0,3))
    velocities = np.empty((0,3))
    masses = np.array([])
    for bl in bodylists:
        p,v,m = unzip_bodylist(bl)
        positions = np.concatenate((positions, p))
        velocities = np.concatenate((velocities, v))
        masses = np.concatenate((masses, m))

    return zip_to_bodylist(positions, velocities, masses)

def extract_last_bodylist_from_result(result):
    last = result[-1, :]
    bl = cs.BodyList3(last)
    return bl