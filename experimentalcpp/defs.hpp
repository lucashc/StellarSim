#ifndef DEFS
#define DEFS
#include <vector>
#include <utility>
#include <algorithm>
#include <cmath>

#define BASETYPE float

class bool3 {
public:
    bool x, y, z;
    bool3() : x(false), y(false), z(false) {};
    bool3(const bool x, const bool y, const bool z) : x(z), y(y), z(z) {};
    // Some basic operations
    inline bool any() {
        return x || y || z;
    }
    inline bool all() {
        return x && y && z;
    }
    inline bool operator==(bool3 b) {
        return x == b.x && y == b.y && z == b.z;
    }
    inline int get_octant() {
        // Use binary to get unique id
        return 1*x + 2*y + 4*z;
    }
};


template <class T>
class vec3_{
public:
    T x,y,z;
    vec3_<T>() : x{0}, y{0}, z{0}{};
    vec3_<T>(const T x, const T y, const T z) : x(x), y(y), z(z) {};
    inline vec3_<T> operator+(const vec3_<T>& v) {
        return vec3_<T>(this->x+v.x, this->y+v.y, this->z+v.z);
    }
    inline vec3_<T> operator-(const vec3_<T>& v) {
        return vec3_<T>(this->x-v.x, this->y-v.x, this->z-v.z);
    }
    inline vec3_<T>operator*(const T x) {
        return vec3_<T>(this->x*x, this->y*x, this->z*x);
    }
    inline T operator*(const vec3_<T> v) {
        return this->x * v.x + this->y * v.y + this->z * v.z;
    }
    inline vec3_<T>operator/(const T x) {
        return vec3_<T>(this->x/x, this->y/x, this->z/x);
    }
    inline void operator+=(const vec3_<T> v) {
        this->x += v.x;
        this->y += v.y;
        this->z += v.z;
    }
    inline bool3 operator>(const vec3_<T>&v) {
        return bool3(this->x > v.x, this->y > v.y, this->z > v.z);
    }
    inline T sum() {
        return this->x+this->y+this->z;
    }
    inline T max() {
        return std::max(this->x, std::max(this->y, this->z));
    }
    inline T norm2() {
        return this->x * this->x + this->y*this->y + this->z*this->z;
    }
    inline T norm() {
        return sqrt(this->norm2());
    }
    inline vec3_<T> abs() {
        return vec3_<T>(std::abs(x), std::abs(y), std::abs(z));
    }
};


typedef vec3_<BASETYPE> vec3;

typedef std::vector<vec3*> veclist;
typedef std::vector<BASETYPE*> scalist;
typedef std::vector<int> intlist;

std::pair<vec3, vec3> get_bounding_vectors(veclist &points) {
    vec3 smallest;
    vec3 largest;
    for (auto p : points) {
        if (p->x < smallest.x) {
            smallest.x = p->x;
        }
        if (p->y < smallest.y) {
            smallest.y = p->y;
        }
        if (p->z < smallest.z) {
            smallest.z = p->z;
        }
        if (p->x > largest.x) {
            largest.x = p->x;
        }
        if (p->y > largest.y) {
            largest.y = p->y;
        }
        if (p->z > largest.z) {
            largest.z = p->z;
        }
    }
    return std::make_pair(smallest, largest);
}

#endif