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

def genEGalaxy(n,M=sc.Msgra,R=1,RD=sc.RDmw/sc.RCmw,space=False,elliptical=False,spiralarms=1):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""

    massarray = md.massSample(n)

    if space == True:
        phi = np.pi/2 - np.random.normal(0,0.1,n)
    else:
        phi = np.pi/2

    if elliptical == True:
        spiral  = 1
        e = 0.5*np.ones(n)+np.random.normal(0,0.005,n)
    else:
        spiral = 0
        e = np.zeros(n)

    r = rd.radSample(n,R,RD)
    for i in range(len(r)):
        if r[i] <= sc.RCmw:
            theta = np.random.uniform(0,2*np.pi,n)
        else:
            theta = (1-spiral) * np.random.uniform(0, 2 * np.pi, n) + spiral * (-2*np.pi*r/np.amax(r)+np.pi/10*np.random.normal(0,1,n)+np.pi*np.random.randint(0,2,n))
    a = r/(1+e)
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    posarray = np.column_stack((x, y, z))
    plt.scatter(x,y)
    plt.show()

    v = np.sqrt(sc.G*(M+massarray)*(2/r-1/a))
    v_x = -np.sin(theta) * v
    v_y = np.cos(theta) * v
    v_z = np.zeros(n)
    velarray = np.column_stack((v_x, v_y, v_z))
    plt.scatter(v_x, v_y)
    plt.show()



    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=M)]
    for i in range(1,n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    return cs.BodyList3(np.array(bodies))

thetamax = 0.5

n_steps = 500  # int(30/1e-4)
begin = time.time()
result = cs.LeapFrogSaveC(genEGalaxy(2,sc.Msgra,space=True,elliptical=True,spiralarms=2), 1e12, n_steps, thetamax, sc.G)
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
    plt.savefig(str(i+1)+'.png')
    print(i)
