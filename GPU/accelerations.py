#!/usr/bin/env python

import numpy as np
import pyopencl as cl
import pyopencl.array
from pyopencl.elementwise import ElementwiseKernel

n = 100
a_np = np.ones((n, 2)).astype(np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_g = cl.array.to_device(queue, a_np)

lin_comb = ElementwiseKernel(ctx,
    "float k1, float *a_g, float k2, float *res_g",
    "res_g[i] = k1 * a_g[i, 0] + k2 * a_g[i, 1]",
    "lin_comb"
)

res_g = cl.array.empty_like(a_g)
lin_comb(2, a_g, 3, res_g)

print(res_g.get())