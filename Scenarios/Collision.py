from helper_files.galaxy_creator import create_andromeda, create_milky_way
import barneshut_cpp.cppsim as cs
import helper_files.stellarConstants as sc

cs.set_thread_count(8)


# Load galaxies
MW = cs.Result.load_last("MWMature.binv")
AM = cs.Result.load_last("AMMature.binv")

# Set collision course


CC = MW + AM

result = cs.LeapFrogSaveC(CC, dt=1e12, n_steps=10000, thetamax=0.7, G=sc.G, save_every=100, epsilon=4e16)
result.save("Collision.binv")