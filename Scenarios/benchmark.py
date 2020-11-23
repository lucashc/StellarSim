import barneshut_cpp.cppsim as cs
import numpy as np
import helper_files.sim_utils as utils
import time

thetamax = 0.5
G = 1
n_steps = 1500
dt = 1e-1

center1 = np.array([400, 0, 0])
center2 = np.array([-400, 0, 0])
v1 = np.array([-3, 0.6, 0])
v2 = -v1  # equal masses => total momentum 0
m_BH = 100000   # mass of black hole

positions = [np.zeros(3)]
velocities = [np.zeros(3)]
masses = [m_BH]
for r in np.arange(1, 30)*25:      # add stars in rings around black hole
    for theta in np.linspace(0, 2*np.pi, int(3*r/25))[:-1]:
        positions.append(np.array([r*np.sin(theta), r*np.cos(theta), 0]))
        velocities.append(np.array([np.cos(theta), -np.sin(theta), 0])*np.sqrt(G*m_BH/r))
        masses.append(10)

positions = np.array(positions)
velocities = np.array(velocities)
N = len(positions)
all_pos = np.concatenate((positions + center1, positions + center2))
all_vel = np.concatenate((velocities + v1, velocities + v2))
all_m = masses + masses


total_bodylist = utils.zip_to_bodylist(all_pos, all_vel, all_m)
total_bodylist.check_integrity()

print("Benchmarking collision of 2 galaxies with parameters: ")
print(f"""\
Number of objects:  {N}
dt:                 {dt}
thetamax:           {thetamax}
n_steps:            {n_steps}
G:                  {G}
""")
begin = time.time()
cs.LeapFrogC(total_bodylist, dt, n_steps, thetamax, G)
end = time.time()
print(f"Simulation finished after {end-begin} s")