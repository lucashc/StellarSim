import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helper_files.sim_utils as utils
import time
import helper_files.render as render
import Scenarios.genGalaxy as gg
import helper_files.stellarConstants as sc

thetamax = 0.5

n_steps = 5000  # int(30/1e-4)
N = 10000
begin = time.time()
result = cs.LeapFrogSaveC(gg.genGalaxy(N,sc.Msgra,spherical=True), 1e12, n_steps, thetamax, sc.G, 10)
end = time.time()
print("Simulation finished after", end-begin, "s")

result.save("testsave.binv")
print("Saved")
result = result.numpy()
s = utils.get_positions(result)
masses = utils.get_masses(result)[0]

plane = render.Plane(np.array([0, 0, 1]), np.array([0, 0, 0]), np.array([5/10**18, 0, 0]), np.array([0, 5/10**18, 0]))
render.animate(s, masses, plane, 400, 400)