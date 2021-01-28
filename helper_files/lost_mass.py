import barneshut_cpp.cppsim as cs
import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc

bl = cs.Result.load_last("last_frame_collision.binv")
# cs.Result(bl).save("last_frame_collision.binv")
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

center = sum([b.pos for b in vis])/len(vis)
M = sum([b.mass for b in vis])
COM = sum([b.mass*b.pos for b in vis])/M
# plt.hist([np.linalg.norm(b.pos-center) for b in vis], bins=200)
# plt.boxplot([np.linalg.norm(b.pos-center) for b in vis])
# plt.show()

new_radius = np.sqrt(sc.Rmw**2 + sc.Randr**2)
filtered  = list(filter(lambda b: abs(np.dot(b.vel, b.pos - COM))/np.linalg.norm(b.pos - COM) < np.sqrt(2*abs(np.dot(b.g, b.pos - COM))), vis))
star_ratio = len(filtered)/len(vis)
mass_ratio = sum([b.mass for b in filtered])/sum([b.mass for b in vis])
print(star_ratio, mass_ratio)