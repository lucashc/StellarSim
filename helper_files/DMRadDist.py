import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import time


def DMradPDF(r, rho0=1, Rs=1, c=12):
    """Navarro-Frenk-White probability density function for radial distance of dark matter particles."""
    normalise = 4*np.pi*rho0*Rs**3*(np.log(1+c)-c/(1+c))
    if r < c*Rs:
        p = rho0*Rs/(r*(1+r/Rs)**2)*4*np.pi*r**2
        return p/normalise
    else:
        return 0
"""
a=50
x = np.linspace(0.001,a,1000*a)
y = np.zeros(len(x))
for i in range(len(x)):
    y[i] = DMradPDF(x[i])
plt.plot(x,y,color="red")
plt.xlabel("$r$ (in units of $R_c$)")
plt.ylabel("$f_{R_c,R_d}(r)$")
plt.grid()
plt.show()
"""

def DMradSample(size=1, rho0=1, Rs=1, c=12):
      """Returns n samples from radial distribution described by DMradPDF."""
      samples=[]
      while len(samples) < size:
          r = np.random.uniform(low=0,high=c*Rs)
          prop = DMradPDF(r, rho0, Rs, c)
          if np.random.uniform(low=0,high=1) <= prop:
              samples += [r]

      return np.array(samples)*sc.RCmw

"""
sample = DMradSample(10000)
binwidth=10000000000000000
plt.hist(sample,bins=np.arange(min(sample), max(sample) + binwidth, binwidth))
plt.show()
"""
