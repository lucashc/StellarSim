import numpy as np

def make_body_array(positions, velocity, mass):
    # [body, (3 pos) + (3 vel) + (1 mass)]
    return np.hstack((positions, velocity, np.expand_dims(mass, 1))).astype(np.float32)
