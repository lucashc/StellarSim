import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import time

scale = 1
edge = 12

def NFWradPDF(r, rho0=1, Rs=scale, c=edge):
    """Navarro-Frenk-White probability density function for radial distance of dark matter particles."""
    normalise = 4*np.pi*rho0*Rs**3*(np.log(1+c)-c/(1+c))
    if r < c*Rs:
        p = rho0*Rs/(r*(1+r/Rs)**2)*4*np.pi*r**2
        return p/normalise
    else:
        return 0


def NFWradSample(size=1, rho0=1, Rs=scale, c=edge):
      """Returns n samples from radial distribution described by DMradPDF."""
      samples=[]
      while len(samples) < size:
          r = np.random.uniform(low=0,high=c*Rs)
          prop = NFWradPDF(r, rho0, Rs, c)
          if np.random.uniform(low=0,high=1) <= prop:
              samples += [r]

      return np.array(samples)*sc.RCmw




def PIradPDF(r, Rc=scale, R_halo=edge):
    """Pseudo-isothermal probability density function for radial distance of dark matter particles."""
    normalise = (4 * np.pi * Rc ** 3 * (R_halo / Rc - np.arctan(R_halo / Rc)))
    if r < R_halo:
        return 1/(1+(r/Rc)**2)*4*np.pi*r**2/normalise
    else:
        return 0


def PIradSample(size, Rc=sc.RCmw, R_halo = 12*sc.RCmw): # bulge radius & halo radius
      """Returns n samples from radial distribution described by PIradPDF."""
      samples = []
      while len(samples) < size:
          r = np.random.uniform(low=0, high=R_halo/Rc)
          prop = PIradPDF(r, 1, R_halo/Rc)
          if np.random.uniform(low=0, high=1) <= prop:
              samples += [r]

      return np.array(samples) * Rc

x = PIradSample(10000)
binwidth = sc.RCmw/10
plt.hist(x,bins=np.arange(min(x), max(x) + binwidth, binwidth))
plt.show()
"""
a=edge
x = np.linspace(0.001,a,1000*a)
y = np.zeros(len(x))
for i in range(len(x)):
    y[i] = PIradPDF(x[i])
plt.plot(x,y,color="red")
plt.xlabel("$r$ (in units of $R_c$)")
plt.ylabel("$f_{R_c,R_d}(r)$")
plt.grid()
plt.show()

a=12
x = np.linspace(0.001,a,1000*a)
y = np.zeros(len(x))
for i in range(len(x)):
    y[i] = PIradPDF(x[i])
plt.plot(x,y,color="red")

sample = PIradSample(10000)/sc.RCmw
binwidth=1e19/sc.RCmw
plt.hist(sample,bins=np.arange(min(sample), max(sample) + binwidth, binwidth),density=True)
plt.show()
"""