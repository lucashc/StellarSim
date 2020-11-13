#include "geometry.hpp"
#include "tree.cpp"
#include <cmath>

void treewalk(OctNode node, OctNode node0, float thetamax, float G){
    float dx = node.COM - node0.COM;
    float r = sqrt((dx*dx).sum());
    if (r>0){
        if(node.children.size() ==0 || node.size/r < thetamax){
            node0.g = node0.g + G * node.mass * dr/r**3
        }
        else{
            for(auto child: node.children){
                treewalk(child, node0, thetamax, G)
            }
        }
    }
}