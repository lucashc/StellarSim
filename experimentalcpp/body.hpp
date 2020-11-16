#ifndef BODY
#define BODY

#include "basetypes.hpp"

class Body {
    vec3 pos, vel;
    BASETYPE mass;
    Body() : pos(), vel(), mass(1) {};
    Body(vec3 pos, vec3 vel, BASETYPE mass) : pos(pos), vel(vel), mass(mass) {};
};


typedef std::vector<Body*> bodylist;


bodylist zip_to_bodylist(veclist points, veclist velocities, scalist masses) {  // no check for equal length, use at own discretion
    bodylist bodies;
    int n = points.size();
    for (int i; i < n; i++) {
        bodies.push_back(&Body(*points[i], *velocities[i], masses[i]));
    }
}
#endif