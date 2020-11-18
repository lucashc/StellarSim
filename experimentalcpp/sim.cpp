#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"


void accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G) {
    auto bounds = get_bounding_vectors(bodies);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first-bounds.second).abs().max();
    std::cout << max_size << std::endl;
    auto topnode = new OctNode(center, max_size, bodies);
    for (auto  b : bodies) {
        TreeWalk(topnode, b, thetamax, G);
    }
    delete topnode;
}


void EulerForward(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G){
    for(int step = 0; step < n_steps; step++){
        std::cout << std::endl;
        std::cout << "Euler forward step " << step << std::endl;
        accelerations(bodies, thetamax, G);
        for(auto body : bodies){
            body->vel = body->vel + body->g * body->mass * dt;
            body->pos = body->pos + body->vel * dt;
        }
    }
}

bodylist copy_bodylist(bodylist &bodies){
    bodylist copy;
    for(auto b : bodies){
        Body* body_copy = new Body(b);
        copy.push_back(body_copy);
    }
    return copy;
}


std::vector<bodylist> EulerForwardSave(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G){
    std::vector<bodylist> save_list;
    save_list.push_back(copy_bodylist(bodies));   // save initial state
    for(int step = 0; step < n_steps; step++){
        accelerations(bodies, thetamax, G);
        for(auto body: bodies){
            body->vel = body->vel + body->g * body->mass * dt;
            body->pos = body->pos + body->vel * dt;

        }

        save_list.push_back(copy_bodylist(bodies));   // save bodies after a step
    }
    return save_list;
}