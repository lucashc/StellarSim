#include "basetypes.hpp"
#include "tree.cpp"
#include <cmath>
#include <vector>

void TreeWalk(OctNode* node, OctNode* node0, float thetamax, float G) {
    vec3 dr = node->COM - node0->COM;
    float r = dr.norm();
    if (r > 0) {
        if (node->children.empty() || node->size / r < thetamax) {
            node0->g = node0->g + dr * G * node->mass / pow(r, 3);
        }
        else {
            for (auto child : node->children) {
                TreeWalk(child, node0, thetamax, G);
            }
        }
    }
}

