import numpy as np
import pyopencl as cl
import pyopencl.array
from pyopencl.elementwise import ElementwiseKernel


class GPU:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(ctx)

    def applyAccelerations(self, bodies):
        accelerations = ElementwiseKernel(self.ctx, 
            "int length, float *bodies, "
        )