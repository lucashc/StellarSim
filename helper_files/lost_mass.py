import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
from mpl_toolkits.mplot3d import Axes3D

bl = cs.Result.load_last("collisionctd.binv")
cs.Result(bl).save("last_frame_collisionctd.binv")
# result = cs.LeapFrogSaveC(bl, dt=1e13, n_steps=3000, thetamax=0.7, G=sc.G, save_every=10, epsilon=4e16)
# result.save("collisionctd.binv")
# bl = cs.Result.load_last("collisionctd.binv")
vis = [b for b in bl if not b.dark_matter]
dm = [b for b in bl if b.dark_matter]
# avg_pos = sum([b.pos for b in bl])/len(bl)
# avg_pos_vis = sum([b.pos for b in bl if not b.dark_matter])/len([1 for b in bl if not b.dark_matter])
# avg_pos_DM = sum([b.pos for b in bl if b.dark_matter])/len([1 for b in bl if b.dark_matter])

def filter_points(bodylist, crit):
    center = sum([b.pos for b in bodylist])/len(bodylist)
    stddev = np.sqrt(sum([np.linalg.norm(b.pos-center)**2 for b in bodylist]))/len(bodylist)
    # bodylist.sort(key = lambda b: np.linalg.norm(b.pos - center))
    return [b for b in bodylist if np.linalg.norm(b.pos-center) < crit*stddev]


# crit = 
# filtered = filter_points(vis, crit)
# star_ratio = len(filtered)/len(vis)
# mass_ratio = sum([b.mass for b in filtered])/sum([b.mass for b in vis])
# print(star_ratio, mass_ratio)

# center = sum([b.pos for b in vis])/len(vis)
# M = sum([b.mass for b in vis])
# COM = sum([b.mass*b.pos for b in vis])/M
# # plt.hist([np.linalg.norm(b.pos-center) for b in vis], bins=200)
# # plt.boxplot([np.linalg.norm(b.pos-center) for b in vis])
# # plt.show()
# BH_pos = bl[9001].pos
# print(bl[6001].mass, bl[265].mass)
# new_radius = np.sqrt(sc.Rmw**2 + sc.Randr**2)
# star_filter = lambda b: np.dot(b.vel, b.pos - COM)/np.linalg.norm(b.pos - COM) < np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) # or np.linalg.norm(b.pos - COM) < sc.Rmw
# filtered  = list(filter(star_filter, vis))
# star_ratio = len(filtered)/len(vis)
# mass_ratio = sum([b.mass for b in filtered])/sum([b.mass for b in vis])
# print(star_ratio, mass_ratio)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# anti_filtered  = list(filter(lambda b: not star_filter(b), vis))
# fx = [b.pos[0] for b in filtered]
# fy = [b.pos[1] for b in filtered]
# fz = [b.pos[2] for b in filtered]
# afx = [b.pos[0] for b in anti_filtered]
# afy = [b.pos[1] for b in anti_filtered]
# afz = [b.pos[2] for b in anti_filtered]
# ax.scatter(afx,afy,afz, color='r')
# ax.scatter(fx,fy,fz, color='g')
# ax.scatter([BH_pos[0]], [BH_pos[1]], [BH_pos[2]], color='b', marker = '^')
# # ax = fig.add_subplot(122, projection='3d')


# ax.set_xlabel('X')

# ax.set_xlim3d(COM[0]-1e21, COM[0]+1e21)
# ax.set_ylim3d(COM[1]-1e21, COM[1]+1e21)
# ax.set_zlim3d(COM[2]-1e21, COM[2]+1e21)
# plt.show()
# M_filtered = sum([b.mass for b in filtered])
# COM_filtered = sum([b.mass * b.pos for b in filtered])/M_filtered
# plt.subplot(211)
# plt.hist([np.linalg.norm(b.pos - COM_filtered) for b in filtered])
# plt.subplot(212)
# plt.hist([np.linalg.norm(b.pos - COM_filtered) for b in anti_filtered], bins = 2000)
# plt.show()
# print(len(vis))


M = sum([b.mass for b in dm])
COM = sum([b.mass*b.pos for b in dm])/M
DM_filter = lambda b: np.dot(b.vel, b.pos - COM)/np.linalg.norm(b.pos - COM) < np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) # or np.linalg.norm(b.pos - COM) < sc.Rmw
print([np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) for b in vis])
filtered  = list(filter(DM_filter, dm))
star_ratio = len(filtered)/len(dm)
mass_ratio = sum([b.mass for b in filtered])/M
print(star_ratio, mass_ratio)