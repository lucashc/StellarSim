import numpy as np
from matplotlib import pyplot as plt
import barneshut_cpp.cppsim as cs
import time
import helper_files.sim_utils as utils
import helper_files.plotting as plotting
import helper_files.stellarConstants as sc
import helper_files.RadDist as rd
import helper_files.MassDist as md
import helper_files.PhysQuants as pq
from mpl_toolkits import mplot3d

def genGalaxy(n,M=sc.Msgra,R=1,RD=sc.RDmw/sc.RCmw,spherical=False):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed. Notice that R and RD are in units of Milky Way galactic bulge radii."""

    theta = np.random.uniform(0, 2 * np.pi, n)
    r = rd.radSample(R,RD,n)
    if spherical == True:
        phi = np.zeros(n)
        for i in range(n):
            if r[i]/sc.RCmw <= R:
                phi[i] = np.random.uniform(0,np.pi)
            else:
                phi[i] = np.pi/2 - np.random.normal(0,0.1)
    else:
        phi = np.pi/2

    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    posarray = np.column_stack((x, y, z))
    plt.scatter(x,y)
    plt.show()

    v = np.sqrt(sc.G*M*(1/r))
    v_x = -np.sin(theta) * v
    v_y = np.cos(theta) * v
    v_z = np.zeros(n)
    velarray = np.column_stack((v_x, v_y, v_z))
    plt.scatter(v_x, v_y)
    plt.show()

    massarray = md.massSample(n)

    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=M)]
    for i in range(1,n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    return cs.BodyList3(np.array(bodies))

thetamax = 0.5

n_steps = 100  # int(30/1e-4)
begin = time.time()
result = cs.LeapFrogSaveC(genGalaxy(1000,sc.Msgra,R=1,spherical=True), 1e14, n_steps, thetamax, sc.G)
end = time.time()


s = utils.get_positions(result)
print(s)
print(s[100])
plt.scatter(s[0][:,0],s[0][:,1])
plt.show()

large_xyz = 1e20
medium_xyz = 1e19

large_limits = {"xlim": (-large_xyz, large_xyz), "ylim": (-large_xyz, large_xyz), "zlim": (-large_xyz, large_xyz)}
medium_limits = {"xlim": (-medium_xyz, medium_xyz), "ylim": (-medium_xyz, medium_xyz), "zlim": (-medium_xyz, medium_xyz)}
# plotting.movie3d(s, np.arange(2), until_timestep=1000, skip_steps=10, mode="line", **medium_limits)

until_timestep = int(n_steps)
starting_angle = 225  # default 270, 0 for sun zoom
rotation_speed = 0  # default 40
elevation = 45  # default 0
def data_gen(index):
    ax.clear()
    #ax.axis('off')
    ax.grid('off')
    plot = ax.scatter3D(s[index][:,0], s[index][:,1], s[index][:,2])
    ax.set(**medium_limits)
    ax.view_init(elev=elevation, azim=index/until_timestep*rotation_speed + starting_angle)
    return plot

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
data_gen(1)
plt.show()

for i in range(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    data_gen(i)
    plt.savefig(str(i)+'.png')
    print(i)
