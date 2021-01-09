import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import time


def NFWradPDF(r, rho0=1, Rs=1, c=12):
    """Navarro-Frenk-White probability density function for radial distance of dark matter particles."""
    normalise = 4*np.pi*rho0*Rs**3*(np.log(1+c)-c/(1+c))
    if r < c*Rs:
        p = rho0*Rs/(r*(1+r/Rs)**2)*4*np.pi*r**2
        return p/normalise
    else:
        return 0


def NFWradSample(size=1, rho0=1, Rs=1, c=12):
      """Returns n samples from radial distribution described by DMradPDF."""
      samples=[]
      while len(samples) < size:
          r = np.random.uniform(low=0,high=c*Rs)
          prop = NFWradPDF(r, rho0, Rs, c)
          if np.random.uniform(low=0,high=1) <= prop:
              samples += [r]

      return np.array(samples)*sc.RCmw




def PIradPDF(r, DM_mass, rho0, Rc=sc.RCmw, R_halo = 3*sc.Rmw):
    """Navarro-Frenk-White probability density function for radial distance of dark matter particles."""
    if r < 1:
        r *= R_halo
        p = rho0/(1+(r/Rc)**2)*4*np.pi*r**2
        return p/DM_mass
    else:
        return 0


def PIradSample(size, DM_mass, Rc=sc.RCmw, R_halo = 3*sc.Rmw):
      """Returns n samples from radial distribution described by DMradPDF."""
      samples=[]
      rho0 = DM_mass/(4*np.pi*sc.G*Rc**3*(R_halo/Rc - np.arctan(R_halo/Rc)))
      while len(samples) < size:
            r = np.random.uniform(low=0,high=1)
            prop = PIradPDF(r, DM_mass, rho0, Rc, R_halo)
            if np.random.uniform(low=0,high=1) <= prop:
                samples += [r]

      return np.array(samples)*sc.RCmw

print(PIradSample(10, sc.MDMmw))