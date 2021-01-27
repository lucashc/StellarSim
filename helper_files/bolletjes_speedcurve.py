import barneshut_cpp.cppsim as cs
import numpy as np
import helper_files.galaxy_creator as gc 
import helper_files.stellarConstants as sc
import matplotlib.pyplot as plt
import helper_files.PhysQuants as pq

cs.set_thread_count(8)
MW = gc.create_milky_way(3000, 6000, R_halo=3*sc.Rmw)



result = cs.LeapFrogSaveC(MW, dt=1e12, n_steps=3000, thetamax=0.7, G=sc.G, save_every=10, epsilon=4e16)
result.save("bsc.binv")
last = cs.Result.load_last("bsc.binv")
r = []
v = []
for b in last:
    if not b.dark_matter:
        r.append(np.linalg.norm(b.pos))
        v.append(np.linalg.norm(b.vel))
        g.append(np.linalg.norm(b.g))

rv = list(zip(r,v,g))
rv.sort(key=lambda x: x[0])
r = [x[0] for x in rv]
v = [x[1] for x in rv]
g = [x[2] for x in rv]

avg = np.convolve(v, np.ones(20), 'valid')/20
print(len(avg), len(v))
plt.plot(r[10:-9], avg, 'r')

plt.scatter(r,v)
plt.xlim((0,sc.Rmw))
plt.show()

# result = cs.Result.load("bsc.binv")
# pq.quantities(result)