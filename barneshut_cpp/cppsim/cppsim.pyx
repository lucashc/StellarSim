# distutils: language=c++
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
cimport cython

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
    # This class is by value, so deallocation of this class, deallocates the underlying object
    cdef Body body

    def __init__(self, np.ndarray[double] pos=np.array([0,0,0], dtype=np.double), np.ndarray[double] vel=np.array([0,0,0], dtype=np.double), double mass=0):
        self.body = Body(vec3(pos[0], pos[1], pos[2]), vec3(vel[0], vel[1], vel[2]), mass)
    
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


Body3_t = np.dtype(Body3)

cdef class BodyList3:

    # This class holds a vector of pointers to Body objects
    # To prevent possible deallocation strict memory management is required
    cdef bodylist bl
    # Save references here to prevent deallocation
    cdef object[:] b

    def __init__(self, np.ndarray[object] b):
        if b.dtype != Body3_t:
            raise TypeError("Not a Body3 type")
        self.bl.reserve(b.shape[0])
        cdef Body3 i3
        for i in b:
            # Cast object to Body3 object as to expose cython interface for pointer retrieval
            i3 = <Body3>i
            self.bl.push_back(&i3.body)
        # Save the array in the class as to increase the reference count of the needed objects
        self.b = b
    def __str__(self):
        return "BodyList3(size=" + str(self.bl.size()) + ")"
    
    def __repr__(self):
        return self.__str__()
    
    @cython.boundscheck(False)
    def __getitem__(self, int i):
        # Pass directly from numpy array, to allow mutation and reference
        # Handles own index errors, so boundscheck is unnecessary
        if 0 <= i > self.b.shape[0]:
            raise IndexError("Out of bounds")
        return self.b[i]
    
    @cython.boundscheck(False)
    def __setitem__(self, int i, Body3 b3):
        # Update numpy array directly, to allow copy, as addresses do not change and array is contiguous
        # Also ensures proper reference count
        # Handles own index errors, so boundscheck is unnecessary
        if 0 <= i > self.b.shape[0]:
            raise IndexError("Out of bounds")
        cdef object obj
        obj = <object>b3
        self.b[i] = obj
    
    def __len__(self):
        return self.bl.size()
    


