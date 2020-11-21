import nbody as nb
import numpy as np
b1 = nb.Body3()
b2 = nb.Body3()

print("Object creation: PASSED")

f = nb.BodyList3(np.array([b1, b2]))

print("Bodylist creation: PASSED")

assert (f[0].pos == np.array([0,0,0], dtype=np.double)).all()

b1.pos = np.array([1,2,3], dtype=np.double)

assert (f[0].pos == np.array([1,2,3], dtype=np.double)).all()

print("Updating: PASSED")

del b1

assert (f[0].pos == np.array([1,2,3], dtype=np.double)).all()

print("Reference lock: PASSED")

f[0].pos = np.array([1,2,10], dtype=np.double)



assert (f[0].pos == np.array([1,2,3], dtype=np.double)).all()

print("Deallocation prevention: PASSED")

del f

assert (b2.pos == np.array([0,0,0], dtype=np.double)).all()

print("Memory integrity: PASSED")