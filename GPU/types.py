import numpy as np
import pyopencl as cl


body = np.dtype([('pos', (np.float64, 3)), ('vel', (np.float64, 3)), ('mass', np.float64)])

def make_body_array(positions, velocity, mass):
    # [body, (3 pos) + (3 vel) + (1 mass)]
    result = np.empty(len(positions), dtype=body)
    result['pos'] = positions
    result['vel'] = velocity
    result['mass'] = mass
    return result
