import barneshut_cpp.cppsim as cs
import numpy as np
import helper_files.stellarConstants as sc

k = # Invullen

MW = cs.BodyList3.load("MWMatureFinal.bin")
AM = cs.BodyList3.load("AMMatureFinal.bin")

MW.translate(np.array([-1, 0, 0])*sc.ly*1e6/1.5 + np.array([0,-k/2,0])*sc.Randr)
MW.add_velocity(np.array([1, 0, 0])*225e3/2)

AM.rotate(np.pi/6, np.zeros(3, dtype=np.double), np.array([1,1,0], dtype=np.double))
AM.translate(np.array([1, 0, 0])*sc.ly*1e6/1.5 + np.array([0,k/2,0])*sc.Randr)
AM.add_velocity(np.array([-1, 0, 0])*225e3/2)

CC = MW + AM

result = cs.LeapFrogSaveC(CC, dt=1e13, n_steps=8000, thetamax=0.7, G=sc.G, save_every=300, epsilon=4e16)
result.save("cd{}.binv".format(k))

bl = cs.Result.load_last("cd{}.binv".format(k))
vis = [b for b in bl if not b.dark_matter]
dm = [b for b in bl if b.dark_matter]


M = sum([b.mass for b in bl])
COM = sum([b.mass*b.pos for b in bl])/M
bl_filter = lambda b: np.dot(b.vel, b.pos - COM)/np.linalg.norm(b.pos - COM) < np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) 
filtered  = list(filter(bl_filter, bl))
star_ratio = len(filtered)/len(bl)
mass_ratio = sum([b.mass for b in filtered])/M
print("All matter:", star_ratio, mass_ratio)



M = sum([b.mass for b in vis])
COM = sum([b.mass*b.pos for b in vis])/M
vis_filter = lambda b: np.dot(b.vel, b.pos - COM)/np.linalg.norm(b.pos - COM) < np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) 
filtered  = list(filter(vis_filter, vis))
star_ratio = len(filtered)/len(vis)
mass_ratio = sum([b.mass for b in filtered])/M
print("Visible matter:", star_ratio, mass_ratio)


M = sum([b.mass for b in dm])
COM = sum([b.mass*b.pos for b in dm])/M
DM_filter = lambda b: np.dot(b.vel, b.pos - COM)/np.linalg.norm(b.pos - COM) < np.sqrt(abs(2*np.dot(b.g, b.pos - COM))) 
filtered  = list(filter(DM_filter, dm))
star_ratio = len(filtered)/len(dm)
mass_ratio = sum([b.mass for b in filtered])/M
print("Dark matter:", star_ratio, mass_ratio)