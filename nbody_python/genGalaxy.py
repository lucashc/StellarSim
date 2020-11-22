import numpy as np
from matplotlib import pyplot as plt
import barneshut_cpp.cppsim as cs
import time
import helper_files.sim_utils as utils
import helper_files.plotting as plotting

def genGalaxy(n,M):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""

    theta = np.random.uniform(0, 2 * np.pi, n)
    r = np.random.exponential(1, n)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros(n)
    posarray = np.column_stack((x, y, z))

    v_x = -np.sin(theta)
    v_y = np.cos(theta)
    v_z = np.zeros(n)
    velarray = np.column_stack((v_x, v_y, v_z))

    massarray = np.random.gamma(2, 2, n)

    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=M)]
    for i in range(1,n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    return cs.BodyList3(np.array(bodies))

print(genGalaxy(20,1e6))

thetamax = 0.5
G = 1

n_steps = 3000  # int(30/1e-4)
begin = time.time()
result = cs.LeapFrogSaveC(genGalaxy(2,1e6), 1e-1, n_steps, thetamax, G)
end = time.time()
print("Simulation finished after", end-begin, "s")

s = utils.get_positions(result)
print(s[0])
print(s[0][:,0])
plt.scatter(s[0][:,0],s[0][:,1])
plt.show()

large_limits = {"xlim": (-1000, 1000), "ylim": (-1000, 1000), "zlim": (-1000, 1000)}
medium_limits = {"xlim": (-0.01, 0.01), "ylim": (-0.01, 0.01), "zlim": (-0.01, 0.01)}
plotting.movie3d(s, np.arange(2), until_timestep=1000, skip_steps=10, mode="line", **medium_limits)
