# distutils: language=c++
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector

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
    ctypedef vector[Body*] bodylist


cdef class Body3:

    cdef Body *body
    def __cinit__(self, np.ndarray[double] pos=np.array([0,0,0], dtype=np.double), np.ndarray[double] vel=np.array([0,0,0], dtype=np.double), double mass=0):
        self.body = new Body(vec3(pos[0], pos[1], pos[2]), vec3(vel[0], vel[1], vel[2]), mass)
    
    @property
    def mass(self):
        return self.body.mass
    @mass.setter
    def mass(self, double mass):
        self.body.mass = mass
    
    @property
    def pos(self):
        return np.array([self.body.pos.x, self.body.pos.y, self.body.pos.z])
    @pos.setter
    def pos(self, np.ndarray[double] pos):
        self.body.pos.x = pos[0]
        self.body.pos.y = pos[1]
        self.body.pos.z = pos[2]
    
    @property
    def vel(self):
        return np.array([self.body.vel.x, self.body.vel.y, self.body.vel.z])
    @vel.setter
    def vel(self, np.ndarray[double] vel):
        self.body.vel.x = vel[0]
        self.body.vel.y = vel[1]
        self.body.vel.z = vel[2]
    
    def __repr__(self):
        return f"Body3(pos=[{self.body.pos.x}, {self.body.pos.y}, {self.body.pos.z}], vel=[{self.body.vel.x}, {self.body.vel.y}, {self.body.vel.z}], mass={self.body.mass})"
    
    def __str__(self):
        return  self.__repr__()
    
    def __dealloc__(self):
        del self.body

Body3_t = np.dtype(Body3)

cdef class BodyList3:
    cdef bodylist bl

    def __init__(self, np.ndarray[Body3_t] b):
        if b.dtype != Body3_t:
            raise TypeError("Not a Body3 type")
        