#include <vector>
#include "defs.hpp"
#include <iostream>

class OctNode {
public:
    float mass, size;
    std::vector<OctNode*> children;
    vec3 g, COM, center;
    int id;

    OctNode(vec3 center, float size, scalist &masses, veclist &points, std::vector<OctNode*> leaves) :
            center(center), size{size}, children(), COM(), mass(), g() 
        {
        int n_points = points.size();
        if (n_points == 1) {
            std::cout << "Done with point" << points[0]->x << std::endl;
            leaves.push_back(this);
            COM = *points[0];
            mass = *masses[0];
        } else {
            std::cout << "We have " << n_points << " here" << std::endl;
            generate_children(points, masses, leaves);
            for (auto c : children) {
                mass += c->mass;
                COM += c->COM;
            }
            COM = COM / mass;
        }
    }
    void generate_children(veclist &points, scalist &masses, std::vector<OctNode*> leaves) {
        intlist octants[8];
        for (int i = 0; i < points.size(); i++) {
            // Convert to defined bool3 type to get id
            octants[((bool3)(*points[i] > center)).get_octant()].push_back(i);
        }
        for (int oc = 0; oc < 8; oc++) {
            std::cout << oc << std::endl;
            auto octant = octants[oc];
            if (octant.size() < 1) {
                std::cout << "Nothing in octant " << oc << std::endl;
                continue;
            }
            veclist childp;
            scalist childm;
            for (auto i : octant) {
                childp.push_back(points[i]);
                childm.push_back(masses[i]);
                std::cout << "Putting child " << points[i]->x << std::endl;

            }
            vec3 new_center;
            switch (oc) {
                // false, false, false
                case 0: new_center = center + vec3(-size/2, -size/2, -size/2);
                // true, false, false
                case 1: new_center = center + vec3(size/2, -size/2, -size/2);
                // false, true, false
                case 2: new_center = center + vec3(-size/2, size/2, -size/2);
                // true, true, false
                case 3: new_center = center + vec3(size/2, size/2, -size/2);
                // false, false, true
                case 4: new_center = center + vec3(-size/2, -size/2, size/2);
                // true, false, true
                case 5: new_center = center + vec3(size/2, -size/2, size/2);
                // false, true, true
                case 6: new_center = center + vec3(-size/2, size/2, size/2);
                // true, true, true
                case 7: new_center = center + vec3(size/2, size/2, size/2);
            };
            std::cout << "We are putting " << childm.size() << " children in octant " << oc << " with size "<< size/2 << " and center " << new_center.x << new_center.y << new_center.z << std::endl; 
            children.push_back(new OctNode(new_center, size/2, childm, childp, leaves));
        }
    }
    ~OctNode() {
        for (auto c : children) {
            delete c;
        }
    }
};