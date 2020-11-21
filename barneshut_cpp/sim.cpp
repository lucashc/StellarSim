#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"
// #include <execution>
// #include <algorithm>


void accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G) {
    auto bounds = get_bounding_vectors(bodies);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first-bounds.second).abs().max();
    //std::cout << max_size << std::endl;
    auto topnode = new OctNode(center, max_size, bodies);
    // std::for_each(std::execution::par_unseq, bodies.begin(), bodies.end(), [=](Body *b){
    //     b->g = vec3(0,0,0);
    //     TreeWalk(topnode, b, thetamax, G);
    // });
    for (auto  b : bodies) {
        b->g = vec3(0,0,0);
        TreeWalk(topnode, b, thetamax, G);
        //std::cout << topnode->children.size() << std::endl;
    }
    delete topnode;
}


void LeapFrog(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G){
    for(int step = 0; step < n_steps; step++){
        //std::cout << std::endl;
        //std::cout << "Euler forward step " << step << std::endl;
        accelerations(bodies, thetamax, G);
        for(auto body : bodies){
            body->vel = body->vel + body->g * dt;
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


std::vector<bodylist> LeapFrogSave(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G){
    std::vector<bodylist> save_list;
    save_list.push_back(copy_bodylist(bodies));   // save initial state
    //std::cout << *bodies[0] << std::endl;
    //std::cout << *bodies[1] << std::endl;
    for(int step = 0; step < n_steps; step++){
        accelerations(bodies, thetamax, G);
        for(auto body: bodies){
            //std::cout << *body << std::endl;
            body->vel = body->vel + body->g * dt;
            body->pos = body->pos + body->vel * dt;
        }

        save_list.push_back(copy_bodylist(bodies));   // save bodies after a step
    }
    return save_list;
}