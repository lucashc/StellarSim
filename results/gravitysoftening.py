from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0.01, 3, 300)

eps = 0.1
y = - 1/np.sqrt(0.1**2 + x**2)
y2 = -1/np.sqrt(x**2)
plt.plot(x, y, label="Potential with gravity softening")
plt.plot(x, y2, label="Potential without gravity softening")
plt.xlabel("x (in natural units)")
plt.ylabel("$\Phi$ (in natural units)")
plt.ylim(-30, 0)
plt.xlim(0, 3)
plt.legend(bbox_to_anchor=(0.95,0.2), loc=1, borderaxespad=0)

plt.show()