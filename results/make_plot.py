import numpy as np
import matplotlib.pyplot as plt
import helper_files.stellarConstants as sc
import barneshut_cpp.cppsim as cs
from scipy.optimize import curve_fit

data = cs.Result.load('IV_test_normal.binv').numpy()
first = data[0]

pos = np.linalg.norm(np.array([body.pos for body in first]), axis=1)
vel = np.linalg.norm(np.array([body.vel for body in first]), axis=1)

plt.style.use('dark_background')
plt.plot(pos, vel, '.', color='white')

def f(x, a, b, c):
    return a-np.exp(-b*x+c)

popt, pcov = curve_fit(f, pos, vel)

x = np.linspace(np.min(pos), np.max(pos), 300)
y = f(x, *popt)
plt.plot(x, y, color='blue')

plt.xlim(0, sc.Rmw*1.2)
# plt.ylim(0, 0.1e6)
plt.xlabel("r (m)")
plt.ylabel("v (m/s)")
plt.show()