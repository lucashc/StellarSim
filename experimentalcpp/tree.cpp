#include <vector>
#include "basetypes.hpp"
#include "body.hpp"
#include <iostream>

class OctNode {
public:
    float mass, size;
    std::vector<OctNode*> children;
    vec3 g, COM, center;
    int id;

    OctNode(vec3 center, float size, bodylist &bodies, std::vector<OctNode*> leaves) :
            center(center), size{size}, children(), COM(), mass(), g() 
        {
        int n_points = bodies.size();
        if (n_points == 1) {
            std::cout << "Done with point" << (bodies[0]->pos).x << std::endl;
            leaves.push_back(this);
            COM = bodies[0]->pos;
            mass = bodies[0]->mass;
        } else {
            std::cout << "We have " << n_points << " here" << std::endl;
            GenerateChildren(bodies, leaves);
            for (auto c : children) {
                mass += c->mass;
                COM += c->COM;
            }
            COM = COM / mass;
        }
    }

    void GenerateChildren(bodylist &bodies, std::vector<OctNode*> &leaves){
        int n = bodies.size();
        bodylist octant_bodies[8];  // contains a vector of bodies for each octant
        // veclist octant_points[8];  // contains a vector of points for each octant
        // scalist octant_masses[8];  //          "           masses       "
        vec3 center {this->center};
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
            float i = octant_index & 1;  // gets i,j,k from octant index
            float j = octant_index & 2;  // which we need to calculate the offset dx of the child node
            float k = octant_index & 4;
            float a = 0.5*this->size;
            vec3 dx {(vec3(i, j, k) - vec3(1,1,1)*0.5) * (0.5*this->size)};
            bodylist this_octant_bodies{ octant_bodies[octant_index] };
            OctNode *new_octnode = new OctNode(center + dx, this->size/2, this_octant_bodies, leaves);
            this->children.push_back(new_octnode);
        }
    }
    ~OctNode() {
        for (auto c : children) {
            delete c;
        }
    }
};
