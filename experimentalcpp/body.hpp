#ifndef BODY
#define BODY

#include "basetypes.hpp"

class Body {
    vec3 pos, vel;
    BASETYPE mass;

    Body() : pos(), vel(), mass(1) {};
    Body(vec3 pos, vec3 vel, BASETYPE mass) : pos(pos), vel(vel), mass(mass) {};
};

#endif