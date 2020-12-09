import numpy as np
import helper_files.sim_utils as utils
import barneshut_cpp.cppsim as cs
from copy import copy


def get_v1_r1_pairs(hist, dt):
    pairs = []
    for bh in hist.T:
        r1 = bh[1].pos
        r2 = bh[2].pos
        v32 = bh[2].vel
        g1 = bh[1].g
        v1_1 = 1/dt * (r2 - r1 - 1/2 * g1 * dt**2)
        v1_2 = v32 - 1/2 * g1 * dt**2
        pairs.append((r1, (v1_1, v1_2)))
    return pairs
    




def calculate_error(samples=1):
    # So 2 bodies with r(0) = (0,0,0) and r(0)'=(0,0,0)
    # Velocity: v(-1/2) = (0,0,0) and v(-1/2)'=(0,0,0)
    start = utils.zip_to_bodylist(
        np.array([[0,0,0], [1,0,0]]),
        np.array([[0,0,0], [0,0,0]]),
        np.array([1,1])
    )
    Q1 = cs.LeapFrogSaveC(start, 1e-2, 3, 1).numpy()
    print(get_v1_r1_pairs(Q1, 1e-2))

if __name__ == "__main__":
    calculate_error()
