import helper_files.galaxy_specrend as galaxy_specrend
from helper_files.sim_utils import get_masses
from helper_files.stellarConstants import Tsol, Msol
import numpy as np

def bodies_to_color(bodies):
    masses = [b.mass for b in bodies]
    colors = np.empty(len(bodies), dtype=(np.float32, 3))
    for i in range(len(masses)):
        temp = Tsol*(masses[i]/Msol)**(2.5/4)
        colors[i] = get_color_from_temp(temp)
    return colors

def get_color_from_temp(temp):
    x, y, z = galaxy_specrend.spectrum_to_xyz(galaxy_specrend.bb_spectrum, temp)
    r, g, b = galaxy_specrend.xyz_to_rgb(galaxy_specrend.SMPTEsystem, x, y, z)
    r = min((max(r, 0), 1))
    g = min((max(g, 0), 1))
    b = min((max(b, 0), 1))
    return galaxy_specrend.norm_rgb(r, g, b)