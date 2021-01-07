import numpy as np
import pyopencl as cl
import pyopencl.array
from pyopencl.elementwise import ElementwiseKernel
from .types import body
from tqdm import tqdm


class GPU:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        
        # Register custom body type
        body_struct, body_struct_c = cl.tools.match_dtype_to_c_struct(self.ctx.devices[0], 'body', body)
        cl.tools.get_or_register_dtype('body', body_struct)

        # kernels
        self.getAccelerations = ElementwiseKernel(self.ctx, 
            "int n_bodies, body *bodies, double *acc, double G",
            """
            double gx = 0, gy = 0, gz = 0;
            for (int j = 0; j < n_bodies; j++) {
                if (i == j) continue;
                double rx = bodies[j].pos[0]-bodies[i].pos[0];
                double ry = bodies[j].pos[1]-bodies[i].pos[1];
                double rz = bodies[j].pos[2]-bodies[i].pos[2];
                double dr = rsqrt(rx*rx + ry*ry + rz*rz);
                double dr3 = dr * dr * dr;
                gx += G * rx * bodies[j].mass * dr3;
                gy += G * ry * bodies[j].mass * dr3;
                gz += G* rz * bodies[j].mass * dr3;
            }
            acc[i*3 + 0] = gx;
            acc[i*3 + 1] = gy;
            acc[i*3 + 2] = gz;
            """,
            "get_accelerations", preamble=body_struct_c
        )

        self.updateVelocities = ElementwiseKernel(self.ctx, 
            "int n_bodies, body *bodies, double G, double dt",
            """
            double gx = 0, gy = 0, gz = 0;
            for (int j = 0; j < n_bodies; j++) {
                if (i == j) continue;
                double rx = bodies[j].pos[0]-bodies[i].pos[0];
                double ry = bodies[j].pos[1]-bodies[i].pos[1];
                double rz = bodies[j].pos[2]-bodies[i].pos[2];
                double dr = sqrt(rx*rx + ry*ry + rz*rz);
                double dr3 = dr * dr * dr;
                gx += G * rx * bodies[j].mass / dr3;
                gy += G * ry * bodies[j].mass / dr3;
                gz += G * rz * bodies[j].mass / dr3;
            }
            bodies[i].vel[0] += gx*dt;
            bodies[i].vel[1] += gy*dt;
            bodies[i].vel[2] += gz*dt;
            """,
            "update_velocity", preamble=body_struct_c
        )

        self.updatePositions = ElementwiseKernel(self.ctx, 
            "body *bodies, double dt",
            """
            bodies[i].pos[0] += bodies[i].vel[0]*dt;
            bodies[i].pos[1] += bodies[i].vel[1]*dt;
            bodies[i].pos[2] += bodies[i].vel[2]*dt;
            """,
            "update_positions", preamble=body_struct_c
        )


    def LeapFrog(self, b, dt, n_steps, G):
        bodies = cl.array.to_device(self.queue, b)
        # Half timestep
        self.updateVelocities(len(b), bodies, G, -dt/2).wait()
        for i in tqdm(range(n_steps)):
            self.updateVelocities(len(b), bodies, G, dt).wait()
            self.updatePositions(bodies, dt).wait()
        self.updateVelocities(len(b), bodies, G, dt/2).wait()
        return bodies.get()
    
    def LeapFrogSave(self, b, dt, n_steps, G, every_step=1):
        saves = np.empty(((n_steps-1)//every_step+1, len(b)), dtype=body)
        bodies = cl.array.to_device(self.queue, b)
        # Half timestep
        self.updateVelocities(len(b), bodies, G, -dt/2)
        for i in tqdm(range(n_steps)):
            self.updateVelocities(len(b), bodies, G, dt)
            self.updatePositions(bodies, dt)
            if i % every_step == 0:
                saves[i//every_step] = bodies.get()
        self.updateVelocities(len(b), bodies, G, dt/2)
        return saves



