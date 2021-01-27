from helper_files.galaxy_creator import create_andromeda, create_milky_way
import barneshut_cpp.cppsim as cs
import helper_files.stellarConstants as sc

cs.set_thread_count(8)



# Milky Way

MW = create_milky_way(4000, 8000)
result = cs.LeapFrogSaveC(MW, dt=1e12, n_steps=10000, thetamax=0.7, G=sc.G, save_every=100, epsilon=4e16)
result.save("MWMature.binv")

# Andromeda

AM = create_andromeda(int(4000*1.25), int(8000*1.25))
result = cs.LeapFrogSaveC(AM, dt=1e12, n_steps=10000, thetamax=0.7, G=sc.G, save_every=100, epsilon=4e16)
result.save("AMMature.binv")