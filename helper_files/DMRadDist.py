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

# def radSample(size=1, R=1, RD=sc.RDmw/sc.RCmw, length_guess=250, rad_min=0):
#     """Returns n samples from radial distribution described by radPDF. Length guess is your best guess for the
#         reciprocal of the probability that a uniform sample is kept, for standard params this is about 250"""
#     radPDF_v = np.vectorize(radPDF)
#     samples = np.empty(0)
#     normalise = -4 * (((R ** 0.75 / RD) ** 3 * R ** 0.75 + 3 * (R ** 0.75 / RD) ** 2 * R ** 0.5 + 6 * (
#                 R ** 0.75 / RD) * R ** 0.25 + 6) * np.exp(-(R ** 0.75 / RD) * R ** 0.25) - 6) / (
#                             R ** 0.75 / RD) ** 4 + RD * np.exp(-R / RD)
#
#     while len(samples) < size:
#         append_length = length_guess*(size - len(samples))
#         unif_samples = np.random.uniform(low=rad_min, high=5 * RD, size=append_length)
#         prop = radPDF_v(unif_samples, R, RD)/normalise
#         keep_sample = np.random.uniform(low=0, high=1, size=append_length) <= prop
#         samples = np.concatenate((samples, unif_samples[keep_sample]))
#
#     return samples[:size]*sc.RCmw