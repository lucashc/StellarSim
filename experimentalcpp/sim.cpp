#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"


void accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G) {
    veclist points;
    for (auto body : bodies) {
        points.push_back(&body->pos);
    }
    auto bounds = get_bounding_vectors(points);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first-bounds.second).abs().max();
    std::cout << max_size << std::endl;
    auto topnode = new OctNode(center, max_size, bodies);
    for (auto  b : bodies) {
        TreeWalk(topnode, b, thetamax, G);
    }
    delete topnode;
    return;
}