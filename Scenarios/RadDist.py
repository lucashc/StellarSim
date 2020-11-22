import numpy as np
import matplotlib.pyplot as plt

def radPDF(x,R=1,RD=1):
    normalise = -4*(((R**0.75/RD)**3*R**0.75+3*(R**0.75/RD)**2*R**0.5+6*(R**0.75/RD)*R**0.25+6)*np.exp(-(R**0.75/RD)*R**0.25)-6)/(R**0.75/RD)**4 + RD*np.exp(-R/RD)
    if x < R:
        return  np.exp(-R**0.75*x**0.25/RD)/normalise
    else:
        return np.exp(-x/RD)/normalise

def radSample(R=1,RD=1,size=None):
    samples=[]
    while len(samples) < size:
        x = np.random.uniform(low=0,high=5*RD)
        prop = radPDF(x,R,RD)
        assert prop >= 0 and prop <= 1
        if np.random.uniform(low=0,high=1) <= prop:
            samples += [x]
    return np.array(samples)

