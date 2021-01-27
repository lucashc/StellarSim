import helper_files.galaxy_creator as gc
import barneshut_cpp.cppsim as cs
import helper_files.stellarConstants as sc
import numpy as np

cs.set_thread_count(8)
MW = gc.create_milky_way(1500, 3000)
MW.translate(np.array([-1, 0, 0])*sc.ly*1e6/2 + np.array([0, 2, 0])*sc.ly*1e5)
MW.add_velocity(np.array([1, 0, 0])*225e3/2)
AM = gc.create_andromeda(1500, 3000)
AM.translate(np.array([1, 0, 0])*sc.ly*1e6/2 - np.array([0, 2, 0])*sc.ly*1e5)
AM.add_velocity(np.array([-1, 0, 0])*225e3/2)
Collision = MW + AM
result = cs.LeapFrogSaveC(Collision, dt=1e13, n_steps=8000, thetamax=0.7, G=sc.G, save_every=10, epsilon=4e16)
result.save("collision.binv")