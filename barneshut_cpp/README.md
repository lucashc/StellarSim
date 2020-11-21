# How to use the Python interface?
Prerequisites: 
* Numpy
* Cython
* Make
* g++ compiler

First build the module: `make build` from this directory. Then the module `barnes_hut` should be importable from the workspace.

This interface exposes:
* `Body`-objects, alias of `Body3`
* `Bodylist`-objects, alias of `Bodylist3`
* `LeapFrogC` and `LeapFrogSaveC` functions for doing integration and using the Barnes Hut algorithm

## Example usage
```python
from barneshut_cpp import Body, Bodylist, LeapFrogSaveC
import numpy as np

n_objects = 2
bodies = np.array([
    Body(), # Initialized at zero
    Body(
        pos=np.array([1,2,3], dtype=np.double), 
        vel=pos=np.array([1,2,3], dtype=np.double), 
        mass=1e4)
])
list_of_bodies = Bodylist(bodies)

dt = 1e-2
n_steps = 1e3
thetamax 0.5
G = 1
# Doing the integration and saving intermediate results
results = LeapFrogSaveC(list_of_bodies, dt, n_steps, thetamax, G)
# Results is a (n_steps, n_objects) shaped numpy array, where each object is a Body-object
```
