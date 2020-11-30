# distutils: language=c++
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libcpp cimport bool
from libcpp.string cimport string
cimport cython


"""
The following are C++ imports required by this Python extension
Add new functions as needed
"""

cdef extern from "basetypes.hpp":
    cdef cppclass vec3 nogil:
        double x, y, z
        vec3()
        vec3(double, double, double)
        bool operator==(const vec3 &v)

cdef extern from "body.hpp":
    cdef cppclass Body nogil:
        vec3 pos, vel, g
        double mass
        Body()
        Body(vec3, vec3, double, vec3)
        Body(Body*)
    ctypedef vector[Body*] bodylist
    void save_bodylist(const bodylist&, string) except +
    bodylist read_bodylist(string) nogil except +
    void save_bodylist_vectorized(const vector[bodylist]&, string) except +
    vector[bodylist] read_bodylist_vectorized(string) nogil except +

cdef extern from "sim.cpp":
    # Can declared nogil, as they 
    void LeapFrog(bodylist&, double, int, double, double) nogil
    vector[bodylist] LeapFrogSave(bodylist&, double, int, double, double, int) nogil
    void accelerated_accelerations(bodylist&, double, double) nogil


cdef class Body3:
    """
    This class represents the Body class from C++. It contains a pointer to the underlying object and 
    all properties of the C++-object have been exported. Deallocation of the underlying object is
    also handled by this class
    """
    cdef Body *body

    def __init__(self, np.ndarray[double] pos=np.array([0,0,0], dtype=np.double), 
            np.ndarray[double] vel=np.array([0,0,0], dtype=np.double), 
            double mass=0, np.ndarray[double] g=np.array([0,0,0], 
            dtype=np.double), make_body_obj=True):
        """
        Initialized the Body3 class
        Args:
            pos, vel, g     | np.ndarray[double] type, default (0,0,0)
            mass            | double, default 0
            make_body_obj   | boolean type, whether to allocate a new Body obj, default is True
                                This option should NOT be changed in Python, only use this in Cython.
        Returns:
            Body3
        """
        if make_body_obj:
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
    """
    This class represents the underlying bodylist object in C++, which is an alias for
    std::vector<Body*>. 
    This class provides strict memory management, by saving a np.ndarray with references of the Body objects,
    as to ensure proper lifetime and existence, by preventing CPython to deallocate them.
    """
    cdef bodylist bl
    cdef object[:] b

    def __init__(self, np.ndarray[object] b=np.array([],dtype=Body3_t)):
        """
        Initializes the BodyList3 class
        Args:
            b | np.ndarray type of Body3 objects
        Returns:
            BodyList3
        """
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
        """
        Loads a .bin file of a saved BodyList3 object.
        Args:
            filename | string type
        Returns:
            BodyList3
        """
        cdef string cpp_filename = filename.encode('UTF-8')
        cdef bodylist bl
        bl = read_bodylist(cpp_filename)
        x = np.empty((bl.size(),), dtype=Body3_t)
        for i in range(bl.size()):
            placeholder = Body3(make_body_obj=False)
            placeholder.body = bl[i]
            x[i] = placeholder
        return BodyList3(x)
    
    def check_integrity(self):
        """
        Checks whether the BodyList3 has proper integrity, meaning that no two objects share the same position.
        If this is the case, the underlying C++ code will cause a segmentation fault, as the recursion limit
        will be exceeded then by the Barnes-Hut algorithm.
        Args: None
        Returns:
            Possible ValueError if integrity check fails
        """
        for i in self.bl:
            for j in self.bl:
                if i !=j and i[0].pos == j[0].pos:
                    raise ValueError("Some bodies are at the same location")
        return
        

BodyList3_t = np.dtype(BodyList3)

def LeapFrogC(BodyList3 bodies, double dt=1e-2, int n_steps=1, double thetamax=0.5, double G=1):
    """
    Executes LeapFrog integration on the accelerations obtained by the Barnes-Hut algorithm.
    This function modifies the given bodies in place.
    Args:
        bodies      | BodyList3 type
        dt          | double type, timestep used for integration
        n_steps     | int type, number of integration steps. Time integrated is: dt*n_steps
        thetamax    | double type, thetamax parameter to Barnes-Hut
        G           | double type, used Newton's coefficient of Gravity
    Returns: None
    """
    cdef bodylist *bl = &bodies.bl
    with nogil:
        LeapFrog(bl[0], dt, n_steps, thetamax, G)


cdef class Result:
    """
    This class represents the result of a simulation as done by LeapFrogSaveC. This class is merely
    a wrapper of the underlying vecto<bodylist> C++-object. To extract the contents, use 
    the numpy() function. This class is not meant to be initialized from Python, 
    only Cython code should initialize this class.
    Important to note: This class wraps a 2D vector of pointers, so deallocating this, will not free the memory.
    So if this class goes out of scope and Python garbage collects this class, it will not free memory and leak. 
    To prevent this, extract the contents with the numpy() method. This creates a numpy array of Body3 objects.
    This will create a reference to the underlying memory, meaning that deleting this array, either by garbage collection
    or del-operator, the memory will be freed. 
    If the numpy array is deleted, this class will be an empty hull of pointers. Calling the numpy() method again
    will result in a segmentation fault. 
    Only ever use the numpy() method once or remember that they all reference the same memory. In addition, one might
    want to use the make_copy parameter.
    """
    cdef vector[bodylist] saves
    
    def numpy(self, make_copy=False):
        """
        Retrieves the simulation results as a numpy array.
        IMPORTANT: Each call to this function will create a reference to the same memory.
        Deallocating one array while another exists will result in a segmentation fault. To prevent this, 
        an explicit copy can be made.
        Args: 
            make_copy | boolean type, whether to make a copy and circumvent memory issues
        Returns:
            np.ndarray[Body3_t] | This is the saved history, with axes: time, object. So it has shape,
                                (saved_frames, len(bodies)).
                                where saved_frames is n_steps//save_every
                                The zeroth step is always saved
        """
        shape = (self.saves.size(), self.saves[0].size())
        save_result = np.empty((self.saves.size(), self.saves[0].size()), dtype=Body3_t)
        for i in range(self.saves.size()):
            for j in range(self.saves[i].size()):
                if make_copy:
                    tmp = new Body(self.saves[i][j])
                    x = Body3(make_body_obj=False)
                    x.body = tmp
                else:
                    x = Body3(make_body_obj=False)
                    x.body = self.saves[i][j]
                save_result[i, j] = x
        return save_result
    
    def save(self, filename):
        """
        Saves a Result object to a file. Preferred extension is: .binv
        This method is incompatible with saving a bodylist.
        Args:
            filename  | string type
        Returns: None
        """
        cdef string cpp_filename = filename.encode('UTF-8')
        save_bodylist_vectorized(self.saves, cpp_filename)
    
    @staticmethod
    def load(filename):
        """
        This staticmethod loads a Result object from file. Preferred extension is .binv
        This mehtod is incompatible with loading a bodylist object.
        Args:
            filename  | string type
        Returns: 
            Result object
        """
        cdef string cpp_filename = filename.encode('UTF-8')
        cdef vector[bodylist] blv = read_bodylist_vectorized(cpp_filename)
        empty_result = Result()
        empty_result.saves = blv
        return empty_result



def LeapFrogSaveC(BodyList3 bodies, double dt=1e-2, int n_steps=1, double thetamax=0.5, double G=1, int save_every=1):
    """
    Executes LeapFrog integration on the accelerations obtained by the Barnes-Hut algorithm.
    This function modifies the given bodies in place. In addition, at each save_every 
    a copy of the bodylist is made.
    Args:
        bodies              | BodyList3 type
        dt                  | double type, timestep used for integration
        n_steps             | int type, number of integration steps. Time integrated is: dt*n_steps
        thetamax            | double type, thetamax parameter to Barnes-Hut
        G                   | double type, used Newton's coefficient of Gravity
        save_every          | int type, each save_every steps a frame is saved
    Returns: 
        Result object, see documentation of this object
    """
    cdef vector[bodylist] saves
    cdef bodylist *bl = &bodies.bl
    with nogil:
        saves = LeapFrogSave(bodies.bl, dt, n_steps, thetamax, G, save_every)
    result = Result()
    result.saves = saves
    return result


def acceleratedAccelerationsC(BodyList3 bodies, double thetamax = 0.5, double G = 1):
    """
    Calculates the accelerations of each body in the bodylist using the Barnes-Hut algorithm. 
    Important: the bodylist is modified in place, its g-attributes are modified
    Args:
        bodies      | BodyList3 type
        thetamax    | double type, thetamax parameter to Barnes-Hut
        G           | double type, used Newton's coefficient of Gravity
    Returns:
        None
    """
    cdef bodylist *bl = &bodies.bl
    with nogil:
        accelerated_accelerations(bl[0], thetamax, G)
