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

        with open('./GPU/program.cl', 'r') as f:
            source = f.read()
        self.program = cl.Program(self.ctx, body_struct_c + source).build()

    def update_velocities(self, bodies, G, dt):
        return self.program.update_velocities(self.queue, (len(bodies),), None, np.int32(len(bodies)), bodies.data, np.double(G), np.double(dt))
    
    def update_positions(self, bodies, dt):
        return self.program.update_velocities(self.queue, (len(bodies),), None, bodies.data, np.double(dt))
    
    def get_accelerations(self, bodies, G):
        bodies = cl.array.to_device(self.queue, bodies)
        acc = cl.array.zeros(self.queue, (len(bodies), 3), np.double)
        self.program.get_accelerations(self.queue, (len(bodies),), None, np.int32(len(bodies)), bodies.data, acc.data, np.double(G))
        return acc.get()
    
    def update(self, bodies, G, dt):
        return self.program.update(self.queue, (len(bodies),), None, np.int32(len(bodies)), bodies.data, np.double(G), np.double(dt))

    def LeapFrog(self, b, dt, n_steps, G):
        bodies = cl.array.to_device(self.queue, b)
        # Half timestep
        self.update_velocities(bodies, G, -dt/2).wait()
        for i in tqdm(range(n_steps)):
            self.update(bodies, G, dt).wait()
        self.update_velocities(bodies, G, dt/2).wait()
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



