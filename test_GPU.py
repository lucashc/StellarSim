from GPU.GPU import GPU
from GPU.types import make_body_array

bodies = make_body_array([[0,0,0], [1,0,0]], [[0,0,0], [0,1,0]], [1,1])

g = GPU()

print(g.applyAccelerations(bodies))