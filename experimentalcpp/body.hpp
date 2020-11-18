#ifndef BODY
#define BODY

#include <ostream>

#include "basetypes.hpp"

class Body {
public:
    vec3 pos, vel, g;
    BASETYPE mass;
    Body() : pos(), vel(), mass(1) {};
    Body(vec3 pos, vec3 vel, BASETYPE mass) : pos(pos), vel(vel), g(), mass(mass) {};
    Body(vec3 pos, vec3 vel, BASETYPE mass, vec3 g) : pos(pos), vel(vel), g(g), mass(mass) {};
    Body(Body* b) : pos(b->pos), vel(b->vel), g(b->g), mass(b->mass) {};
};


std::ostream& operator<<(std::ostream& os, const Body& b) {   // for printing Body objects
    return os << "BODY[pos=" << b.pos << ", vel=" << b.vel << ", m=" << b.mass << ", g=" << b.g << "]";
}

typedef std::vector<Body*> bodylist;


bodylist zip_to_bodylist(veclist points, veclist velocities, scalist masses) {  // no check for equal length, use at own discretion
    bodylist bodies;
    int n = points.size();
    for (int i = 0; i < n; i++) {
        bodies.push_back(new Body(*points[i], *velocities[i], masses[i]));
    }
    return bodies;
}

std::pair<vec3, vec3> get_bounding_vectors(bodylist &points) {
    vec3 smallest;
    vec3 largest;
    for (auto p : points) {
        if (p->pos.x < smallest.x) {
            smallest.x = p->pos.x;
        }
        if (p->pos.y < smallest.y) {
            smallest.y = p->pos.y;
        }
        if (p->pos.z < smallest.z) {
            smallest.z = p->pos.z;
        }
        if (p->pos.x > largest.x) {
            largest.x = p->pos.x;
        }
        if (p->pos.y > largest.y) {
            largest.y = p->pos.y;
        }
        if (p->pos.z > largest.z) {
            largest.z = p->pos.z;
        }
    }
    return std::make_pair(smallest, largest);
}

#endif