#ifndef BODY
#define BODY

#include <ostream>
#include <fstream>
#include <string>

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

void save_bodylist_to_ofstream(const bodylist &bl, std::ofstream &wf) {
    int len = bl.size();
    wf.write((char*) &len, sizeof(int));
    for (auto b : bl) {
        wf.write((char*) b, sizeof(Body));
    }
}

bodylist read_bodylist_from_ifstream(std::ifstream &rf) {
    int len;
    rf.read((char*) &len, sizeof(int));
    bodylist bl;
    for (int i = 0; i < len; i++) {
        Body b;
        rf.read((char*) &b, sizeof(Body));
        bl.push_back(new Body(&b));
    }
    return bl;
}


void save_bodylist(const bodylist &bl, std::string filename) {
    std::ofstream wf(filename, std::ofstream::out | std::ofstream::binary);
    if (!wf) {
        throw "Cannot open file!";
    }
    save_bodylist_to_ofstream(bl, wf);
    wf.close();
    if (!wf.good()) {
        throw "Error writing!";
    }
}

bodylist read_bodylist(std::string filename) {
    std::ifstream rf(filename, std::ofstream::out | std::ofstream::binary);
    if (!rf) {
        throw "Cannot open file!";
    }
    bodylist bl = read_bodylist_from_ifstream(rf);
    rf.close();
    return bl;
}

void save_bodylist_vectorized(std::vector<bodylist> &blv, std::string filename) {
    std::ofstream wf(filename, std::ofstream::out | std::ofstream::binary);
    if (!wf) {
        throw "Cannot open file!";
    }
    int size = blv.size();
    wf.write((char*) &size, sizeof(size));
    for (auto bl : blv) {
        save_bodylist_to_ofstream(bl, wf);
    }
    wf.close();
    if (!wf.good()) {
        throw "Error writing!";
    }
}

std::vector<bodylist> read_bodylist_vectorized(std::string filename) {
    std::ifstream rf(filename, std::ofstream::out | std::ofstream::binary);
    if (!rf) {
        throw "Cannot open file!";
    }
    int size;
    rf.read((char*) &size, sizeof(size));
    std::vector<bodylist> blv;
    for (int i = 0; i < size; i++) {
        bodylist bl = read_bodylist_from_ifstream(rf);
        blv.push_back(bl);
    }
    rf.close();
    return blv;
}

#endif