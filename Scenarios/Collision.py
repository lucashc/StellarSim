from helper_files.galaxy_creator import create_andromeda, create_milky_way
import barneshut_cpp.cppsim as cs
import helper_files.stellarConstants as sc
import numpy as np

cs.set_thread_count(8)


# Load galaxies
MW = cs.Result.load_last("MWMature.binv")
AM = cs.Result.load_last("AMMature.binv")

# Set collision course
MW.translate(np.array([-1, 0, 0])*sc.ly*1e6/1.5)
MW.add_velocity(np.array([1, 0, 0])*225e3/2)

AM.rotate(np.pi/6, np.zeros(3, dtype=np.double), np.array([1,1,0], dtype=np.double))
AM.translate(np.array([1, 0, 0])*sc.ly*1e6/1.5)
AM.add_velocity(np.array([-1, 0, 0])*225e3/2)

CC = MW + AM

result = cs.LeapFrogSaveC(CC, dt=1e13, n_steps=10000, thetamax=0.7, G=sc.G, save_every=100, epsilon=4e16)
result.save("Collision.binv")