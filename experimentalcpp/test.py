import cppsim as cs
import numpy as np
b1 = cs.Body3()
b2 = cs.Body3()

f = cs.BodyList3(np.array([b1, b2]))
print(f)

print(f[0])

b1.pos = np.array([1,2,3], dtype=np.double)

print(f[0])

del b1

print(f[0])
f[0].pos = np.array([1,2,10], dtype=np.double)
print(f[0])
f[0] = cs.Body3()
print(f[0])