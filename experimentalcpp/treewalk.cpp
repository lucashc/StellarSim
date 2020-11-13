#include "geometry.hpp"
#include "tree.cpp"
#include <cmath>
#include <vector>

void TreeWalk(OctNode node, OctNode node0, float thetamax, float G){
    float dx = node.COM - node0.COM;
    float r = sqrt((dx*dx).sum());
    if (r>0){
        if(node.children.size() ==0 || node.size/r < thetamax){
            node0.g = node0.g + G * node.mass * dr/r**3
        }
        else{
            for(auto child: node.children){
                TreeWalk(child, node0, thetamax, G)
            }
        }
    }
}








//    for(int i; i<2; ++i){
//        for(int j; j<2; ++j){
//            for(int k; k<2; ++k){
//                bool[n] in_octant;
//                for(int i; i < n; i++){
//                    in_octant[i] =
//                }
//            }
//        }
//    }

}