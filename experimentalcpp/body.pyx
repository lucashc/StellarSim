# distutils: language=c++

import numpy as np

cdef extern from "basetypes.hpp":
    cdef cppclass vec3:
        double x, y, z
        vec3()
        vec3(double, double, double)

cdef extern from "body.hpp":
    cdef cppclass Body:
        vec3 pos, vel
        double mass
        Body()
        Body(vec3, vec3, double)


cdef class Vector3:
    cdef vec3 vec
    def __init__(self, x=0, y=0, z=0):
        self.vec = vec3(x, y, z)
    @property
    def x(self):
        return self.vec.x
    @x.setter
    def x(self, x):
        self.vec.x = x
    @property
    def y(self):
        return self.vec.y
    @y.setter
    def y(self, y):
        self.vec.y = y
    @property
    def z(self):
        pass



cdef class Body3:

    cdef Body body

    def __init__(self, pos=[0,0,0], vel=[0,0,0], mass=0):
        cdef vec3 pos3, vel3
        pos3 = vec3(pos[0], pos[1], pos[2])
        vel3 = vec3(vel[0], vel[1], vel[2])
        self.body = Body(pos3, vel3, mass)
    
    @property
    def mass(self):
        return self.body.mass
    @mass.setter
    def mass(self, mass):
        self.body.mass = mass
    
    @property
    def pos(self):
        return np.array([self.body.pos.x, self.body.pos.y, self.body.pos.z])
    @pos.setter
    def pos(self, pos):
        self.body.pos.x = pos[0]
        self.body.pos.y = pos[1]
        self.body.pos.z = pos[2]
    
    @property
    def vel(self):
        return np.array([self.body.vel.x, self.body.vel.y, self.body.vel.z])
    @vel.setter
    def vel(self, vel):
        self.body.vel.x = vel[0]
        self.body.vel.y = vel[1]
        self.body.vel.z = vel[2]
    
    def __repr__(self):
        return f"Body(pos=[{self.body.pos.x}, {self.body.pos.y}, {self.body.pos.z}], vel=[{self.body.vel.x}, {self.body.vel.y}, {self.body.vel.z}], mass={self.body.mass})"
    
    def __str__(self):
        return  self.__repr__()