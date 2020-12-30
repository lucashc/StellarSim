import numpy as np
from matplotlib import pyplot as plt
import barneshut_cpp.cppsim as cs
import time
import helper_files.sim_utils as utils
import helper_files.plotting as plotting
import helper_files.stellarConstants as sc
import helper_files.RadDist as rd
import helper_files.MassDist as md
import helper_files.DMRadDist as DMrd
import helper_files.PhysQuants as pq
from mpl_toolkits import mplot3d

def genDMG(n, M=sc.Msgra, R=1, RD=sc.RDmw/sc.RCmw, spherical=False, nDM=0, rho0=1, Rs=1, c=12):
    """Generate a galaxy (Bodylist) of a massive black hole M and n stars, with initial positions, velocities and masses randomly distributed"""

    theta = np.random.uniform(0, 2 * np.pi, n)
    if spherical == True:
        phi = np.pi/2 - np.random.normal(0,0.1,n)
    else:
        phi = np.pi/2
    r = rd.radSample(R,RD,n)
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    posarray = np.column_stack((x, y, z))

    v = np.sqrt(sc.G*M*(1/r))
    v_x = -np.sin(theta) * v
    v_y = np.cos(theta) * v
    v_z = np.zeros(n)
    velarray = np.column_stack((v_x, v_y, v_z))

    massarray = md.massSample(n)

    bodies = [cs.Body3(pos=np.zeros(3), vel=np.zeros(3), mass=M)]
    for i in range(1,n):
        bodies.append(cs.Body3(pos=posarray[i], vel=velarray[i], mass=massarray[i]))

    thetaDM = np.random.uniform(0,2*np.pi,nDM)
    phiDM = np.random.uniform(0,np.pi,nDM)
    rDM = DMrd.DMradSample(nDM, rho0, Rs, c)
    xDM = rDM * np.cos(thetaDM) * np.sin(phiDM)
    yDM = rDM * np.sin(thetaDM) * np.sin(phiDM)
    zDM = rDM * np.cos(phiDM)
    posarrayDM = np.column_stack((xDM, yDM, zDM))

    v_xDM = np.zeros(nDM)
    v_yDM = np.zeros(nDM)
    v_zDM = np.zeros(nDM)
    velarrayDM = np.column_stack((v_xDM, v_yDM, v_zDM))

    massarrayDM = md.massSample(nDM)

    bodiesDM = []
    for i in range(1, nDM):
        bodiesDM.append(cs.Body3(pos=posarrayDM[i], vel=velarrayDM[i], mass=massarrayDM[i]))

    allbodies = np.concatenate((bodies,bodiesDM))

    return cs.BodyList3(np.array(allbodies)), cs.BodyList3(np.array(bodies)), cs.BodyList3(np.array(bodiesDM))

thetamax = 0.5

n_steps = 1000  # int(30/1e-4)
begin = time.time()
# print(genDMG(1000,M=sc.Msgra,spherical=True,nDM=100))
result = cs.LeapFrogSaveC(genDMG(1000,M=sc.Msgra,spherical=True,nDM=10000)[1], 1e12, n_steps, thetamax, sc.G)
end = time.time()


s = utils.get_positions(result)
print(s)
print('test')
print(s[100])
plt.scatter(s[0][:,0],s[0][:,1])
plt.show()

large_xyz = 1e20
medium_xyz = 2*1e19

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
