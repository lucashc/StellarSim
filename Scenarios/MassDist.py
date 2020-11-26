import numpy as np
import matplotlib.pyplot as plt
import Scenarios.stellarConstants as sc


def massPDF(x):
    """Probability density function for star mass."""
    u = x / sc.Msol
    k = 0.158 / (np.log(10)) * np.exp((-np.log10(0.08)) ** 2 / (2 * 0.69 ** 2))
    if u > 1:
        return k * u ** (-2.3)
    else:
        return 0.158 / (np.log(10) * u) * np.exp((-np.log10(u) - np.log10(0.08)) ** 2 / (2 * 0.69 ** 2))

def massSample(size=1):
    """Returns n samples from mass distribution described by massPDF."""
    samples = []
    normalise = 79 / (650 * np.log(10)) * np.exp(-(5000 * (np.log(2 / 25)) ** 2) / (4761 * (np.log(
        10)) ** 2)) + 0.257983437565181  # Output of Integral Calculator with the integral of 0.158/(log(10)*x)*exp(-(log10(x)-log10(0.08))**2/(2*0.69**2)) from 0 to 1 and the integral 0.158/(log(10))*exp(-(-log10(0.08))**2/(2*0.69**2))*x**-2.3 from 1 to \infty.
    while len(samples) < size:
        x = np.random.uniform(low=0.5, high=10)
        prop = massPDF(x*sc.Msol) / normalise
        print(prop)
        #assert prop >= 0 and prop <= 1
        if np.random.uniform(low=0, high=1) <= prop:
            samples += [x]
    return np.array(samples) * sc.Msol
