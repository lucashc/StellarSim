# distutils: language=c++
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libcpp.string cimport string
cimport cython

cdef extern from "basetypes.hpp":
    cdef cppclass vec3:
        double x, y, z
        vec3()
        vec3(double, double, double)

cdef extern from "body.hpp":
    cdef cppclass Body:
        vec3 pos, vel, g
        double mass
        Body()
        Body(vec3, vec3, double, vec3)
    ctypedef vector[Body*] bodylist
    void save_bodylist(const bodylist&, string) except +
    bodylist read_bodylist(string) except +

cdef extern from "sim.cpp":
    void LeapFrog(bodylist&, double, int, double, double)
    vector[bodylist] LeapFrogSave(bodylist&, double, int, double, double) except +


cdef class Body3:
    # This class is by value, so deallocation of this class, deallocates the underlying object
    cdef Body *body

    def __init__(self, np.ndarray[double] pos=np.array([0,0,0], dtype=np.double), 
            np.ndarray[double] vel=np.array([0,0,0], dtype=np.double), 
            double mass=0, np.ndarray[double] g=np.array([0,0,0], 
            dtype=np.double)):
        self.body = new Body(vec3(pos[0], pos[1], pos[2]), vec3(vel[0], vel[1], vel[2]), mass, vec3(g[0], g[1], g[2]))
    
    @property
    def mass(self):
        return self.body.mass
    @mass.setter
    def mass(self, double mass):
        self.body.mass = mass
    
    @property
    def pos(self):
        return np.array([self.body.pos.x, self.body.pos.y, self.body.pos.z], dtype=np.double)
    @pos.setter
    def pos(self, np.ndarray[double] pos):
        self.body.pos.x = pos[0]
        self.body.pos.y = pos[1]
        self.body.pos.z = pos[2]
    
    @property
    def vel(self):
        return np.array([self.body.vel.x, self.body.vel.y, self.body.vel.z], dtype=np.double)
    @vel.setter
    def vel(self, np.ndarray[double] vel):
        self.body.vel.x = vel[0]
        self.body.vel.y = vel[1]
        self.body.vel.z = vel[2]
    
    @property
    def g(self):
        return np.array([self.body.g.x, self.body.g.y, self.body.g.z], dtype=np.double)
    
    @g.setter
    def g(self, np.ndarray[double] g):
        self.body.g.x = g[0]
        self.body.g.y = g[1]
        self.body.g.z = g[2]
    
    def __repr__(self):
        return f"Body3(pos=[{self.body.pos.x}, {self.body.pos.y}, {self.body.pos.z}], vel=[{self.body.vel.x}, {self.body.vel.y}, {self.body.vel.z}], mass={self.body.mass}, g=[{self.body.g.x}, {self.body.g.y}, {self.body.g.z}])"
    
    def __str__(self):
        return  self.__repr__()
    
    def __deallocate__(self):
        del self.body


Body3_t = np.dtype(Body3)

cdef class BodyList3:

    # This class holds a vector of pointers to Body objects
    # To prevent possible deallocation strict memory management is required
    cdef bodylist bl
    # Save references here to prevent deallocation
    cdef object[:] b

    def __init__(self, np.ndarray[object] b=np.array([],dtype=Body3_t)):
        if b.dtype != Body3_t:
            raise TypeError("Not a Body3 type")
        self.bl.reserve(b.shape[0])
        cdef Body3 i3
        for i in b:
            # Cast object to Body3 object as to expose cython interface for pointer retrieval
            i3 = <Body3>i
            self.bl.push_back(i3.body)
        # Save the array in the class as to increase the reference count of the needed objects
        self.b = b
    def __str__(self):
        result = f"BodyList3(size={self.bl.size()}, bodies=["
        result += ", ".join(map(str, self.b))
        result += "])"
        return result
    
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
    
    def save(self, filename):
        cdef string cpp_filename = filename.encode('UTF-8')
        save_bodylist(self.bl, cpp_filename)
    
    @staticmethod
    def load(filename):
        cdef string cpp_filename = filename.encode('UTF-8')
        cdef bodylist bl
        bl = read_bodylist(cpp_filename)
        x = np.empty((bl.size(),), dtype=Body3_t)
        for i in range(bl.size()):
            placeholder = Body3()
            placeholder.body = bl[i]
            x[i] = placeholder
        return BodyList3(x)

    def __add__(self, BodyList3 other):
        self.b
        

BodyList3_t = np.dtype(BodyList3)

def LeapFrogC(BodyList3 bodies, double dt, int n_steps, double thetamax, double G):
    LeapFrog(bodies.bl, dt, n_steps, thetamax, G)


def LeapFrogSaveC(BodyList3 bodies, double dt, int n_steps, double thetamax, double G):
    cdef vector[bodylist] saves
    saves = LeapFrogSave(bodies.bl, dt, n_steps, thetamax, G)
    save_result = np.empty((n_steps+1,len(bodies)), dtype=Body3_t)
    for i in range(saves.size()):
        for j in range(saves[i].size()):
            x = Body3()
            x.body = saves[i][j]
            save_result[i, j] = x
    return save_result
