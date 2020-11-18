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
        accelerations(bodies, thetamax, G);
        for(auto body: bodies){
            body->vel = body->g * dt;
            body->pos = body->vel * dt;
        }
    }
}

bodylist copy_bodylist(bodylist &bodies){
    bodylist copy;
    for(auto b: bodies){
        Body* body_copy = new Body(b);
        copy.push_back(body_copy);
    }
    return copy;
}


bodylist* EulerForwardSave(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G){
    auto save_list = new bodylist[n_steps];
    bodylist updated_bodies[n_steps + 1];
    save_list[0] = copy_bodylist(bodies);   // save initial state
    updated_bodies[0] = bodies;
    for(int step = 0; step < n_steps; step++){
        accelerations(bodies, thetamax, G);
        for(auto body: bodies){
            body->vel = body->g * dt;
            body->pos = body->vel * dt;

        }

        save_list[step + 1] = copy_bodylist(bodies);   // save bodies after a step
    }
    return save_list;
}