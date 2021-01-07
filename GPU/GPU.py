import numpy as np
import pyopencl as cl
import pyopencl.array
from pyopencl.elementwise import ElementwiseKernel


class GPU:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def applyAccelerations(self, b):
        accelerations = ElementwiseKernel(self.ctx, 
            "int n_bodies, int* index_g, float *bodies, float *acc",
            """
            float gx = 0, gy = 0, gz = 0;
            for (int j = 0; j < n_bodies; j++) {
                printf("%d,%d", i, j);
                if (i == j) continue;
                float rx = bodies[i, 0]-bodies[j, 0];
                float ry = bodies[i, 1]-bodies[j, 1];
                float rz = bodies[i, 2]-bodies[j, 2];
                float dr = rsqrt(rx*rx + ry*ry + rx*rz);
                float dr3 = dr * dr * dr;
                gx += rx * bodies[j, 6] * dr3;
                gy += ry * bodies[j, 6] * dr3;
                gz += rz * bodies[j, 6] * dr3;
            }
            acc[i, 0] = gx;
            acc[i, 1] = gy;
            acc[i, 2] = gz;
            """,
            "accelerations"
        )
        index = np.arange(0, len(b)).astype(np.int32)
        index_g = 
        bodies = cl.array.to_device(self.queue, b)
        acc = cl.array.empty(self.queue, (len(b), 3), dtype=np.float32)
        accelerations(len(bodies), bodies, acc)
        return acc.get()
