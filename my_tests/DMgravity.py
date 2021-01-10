import barneshut_cpp.cppsim as cs
import helper_files.sim_utils as utils
import helper_files.stellarConstants as sc
import numpy as np
dummy = utils.make_body([0,0,0], [0,0,0], 0)
A = utils.make_body([1e5,0,0], [0,0,0], 1e21)
#C = utils.make_body([sc.RCmw/100*1.1,0,0], [0,0,0], 1e18)
B = utils.make_body([-1e5, 0,0], [0,0,0], 1e21, dark_matter = True)
#D = utils.make_body([-sc.RCmw/100*1.1,0,0], [0,0,0], 1e18, dark_matter = True)
bl = cs.BodyList3(np.array([A,B,dummy]))

n_steps = 3000
thetamax = 0.7

result = cs.LeapFrogSaveC(bl, dt=0.01, n_steps=n_steps, thetamax=thetamax, G=sc.G*1e3, save_every=10)
result.save('dmgrav.binv')
#print(result.numpy())