import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import time


def radPDF(x, R=1, RD=sc.RDmw/sc.RCmw):
    """Probability density function for radial distance from galaxy centre, with bulge radius R and characteristics scale length RD."""
    if x < R:
        return np.exp(-R**0.75*x**0.25/RD)
    else:
        return np.exp(-x/RD)


def radSample(R=1, RD=sc.RDmw/sc.RCmw, size=1):
    """Returns n samples from radial distribution described by radPDF."""
    samples=[]
    normalise = -4 * (((R ** 0.75 / RD) ** 3 * R ** 0.75 + 3 * (R ** 0.75 / RD) ** 2 * R ** 0.5 + 6 * (
                R ** 0.75 / RD) * R ** 0.25 + 6) * np.exp(-(R ** 0.75 / RD) * R ** 0.25) - 6) / (
                            R ** 0.75 / RD) ** 4 + RD * np.exp(-R / RD)
    while len(samples) < size:
        x = np.random.uniform(low=0,high=5*RD)
        prop = radPDF(x, R, RD)/normalise
        if np.random.uniform(low=0,high=1) <= prop:
            samples += [x]

    return np.array(samples)*sc.RCmw


def radSampleFast(R=1, RD=sc.RDmw/sc.RCmw, size=1, length_guess=250):
    """Returns n samples from radial distribution described by radPDF. Length guess is your best guess for the
        reciprocal of the probability that a uniform sample is kept, for standard params this is about 250"""
    radPDF_v = np.vectorize(radPDF)
    samples = np.empty(0)
    normalise = -4 * (((R ** 0.75 / RD) ** 3 * R ** 0.75 + 3 * (R ** 0.75 / RD) ** 2 * R ** 0.5 + 6 * (
                R ** 0.75 / RD) * R ** 0.25 + 6) * np.exp(-(R ** 0.75 / RD) * R ** 0.25) - 6) / (
                            R ** 0.75 / RD) ** 4 + RD * np.exp(-R / RD)

    while len(samples) < size:
        append_length = length_guess*(size - len(samples))
        unif_samples = np.random.uniform(low=0, high=5 * RD, size=append_length)
        prop = radPDF_v(unif_samples, R, RD)/normalise
        keep_sample = np.random.uniform(low=0, high=1, size=append_length) <= prop
        samples = np.concatenate((samples, unif_samples[keep_sample]))

    return samples[:size]*sc.RCmw