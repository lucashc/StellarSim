import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


data = np.loadtxt('algorithm_comparison.csv', skiprows=1, usecols=(0,1,2), delimiter=';')
n = data[:, 0].astype(np.int)
cpu = data[:, 1]
gpu = data[:, 2]


def nlogn(x, a, b):
    return a*x*np.log(x)+b

def square(x, a, b, c):
    return (b*(x-a))**2+c

poptc, _ = curve_fit(nlogn, n, cpu)

poptg, _ = curve_fit(square, n, gpu)

x = np.linspace(np.min(n), np.max(n), 100)

plt.subplot(121)

plt.plot(x, nlogn(x, *poptc), color='red', label='$n \log(n)$-fit')
plt.scatter(n, cpu, label="Runtimes")
plt.title("Barnes-Hut")
plt.xlabel('$n$')
plt.ylabel("Runtime (s)")
plt.grid()
plt.legend()

plt.subplot(122)

plt.plot(x, square(x, *poptg), color='red', label='$n^2$-fit')
plt.scatter(n, gpu, label='Runtimes')
plt.title("Brute force")
plt.xlabel('$n$')
plt.ylabel("Runtime (s)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()