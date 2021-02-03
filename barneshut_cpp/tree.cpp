#ifndef TREE
#define TREE
#include <vector>
#include "basetypes.hpp"
#include "body.hpp"
#include <iostream>
#include <cmath>

class OctNode {
public:
    BASETYPE mass, dark_matter_mass, size;
    std::vector<OctNode*> children;
    vec3 COM, DM_COM, center;
    Body *id;
    bool leaf;

    OctNode(vec3 center, BASETYPE size, bodylist &bodies) :
            mass(), size(size), children(), COM(), center(center)
        {
        int n_points = bodies.size();
        if (n_points == 1) {
            COM = bodies[0]->pos;
            mass = bodies[0]->mass;
            id = bodies[0];
            leaf = true;
        } else {
            GenerateChildren(bodies);
            for (auto c : children) {
                mass += c->mass;
                COM += c->COM * c->mass;
            }
            COM = COM / mass;
            id = nullptr;
            leaf = false;
        }
        // both mass and COM account for dark matter + normal matter
    }

    void GenerateChildren(bodylist &bodies){
        int n = bodies.size();
        bodylist octant_bodies[8];  // contains a vector of bodies for each octant
        for(int index = 0; index < n; ++index){  // assign each point (and corresponding mass) to an octant
            vec3* point = &bodies[index]->pos;
            int i = point->x > center.x;
            int j = point->y > center.y;
            int k = point->z > center.z;
            int octant_index = 4*k + 2*j + i;  // construct binary number to choose octant
            octant_bodies[octant_index].push_back(bodies[index]);
        }

        for(unsigned int octant_index = 0; octant_index < 8; ++octant_index){  // create child nodes for each octant
            if(octant_bodies[octant_index].empty()){continue;}
            int i = octant_index & 1;  // gets i,j,k from octant index
            int j = (octant_index & 2)/2;  // which we need to calculate the offset dx of the child node
            int k = (octant_index & 4)/4;
            vec3 dx {(vec3(i, j, k) - vec3(1,1,1)*0.5) * (0.5*size)};
            OctNode *new_octnode = new OctNode(center + dx, size/2, octant_bodies[octant_index]);
            children.push_back(new_octnode);
        }
    }
    ~OctNode() {
        for (auto c : children) {
            delete c;
        }
    }
};


void TreeWalk(OctNode* node, Body* b, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon) {
    vec3 dr = node->COM - b->pos;
    BASETYPE r = dr.norm();
    BASETYPE rs = r*r + epsilon*epsilon;
    if (rs > 0) {
        if ((node->leaf || node->size / r < thetamax) && node->id != b) {
            b->g = b->g + (dr / r) * G * node->mass / rs;
        }
        else {
            for (auto child : node->children) {
                TreeWalk(child, b, thetamax, G, epsilon);
            }
        }
    }
};

BASETYPE TreeWalkEnergy(OctNode* node, Body* b, BASETYPE thetamax, BASETYPE G) {
    vec3 dr = node->COM - b->pos;
    BASETYPE r = dr.norm();
    if (r > 0) {
        if ((node->leaf || node->size / r < thetamax) && node->id != b) {
            return -b->mass * G * node->mass / r;
        }
        else {
            BASETYPE U = 0;
            for (auto child : node->children) {
                U += TreeWalkEnergy(child, b, thetamax, G);
            }
            return U;
        }
    }
    return 0;
};

#endif