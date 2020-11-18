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






using namespace std;

int main() {
    auto p = vector<vec3> {vec3(0, 0, 0), vec3(2, 1, 0), vec3(-1, -1, 0), vec3(0, 2, 1) };
    auto m = scalist({100.0, 1.0, 2.0, 123456});
    auto v = vector<vec3>{vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0) };
    veclist p_, v_;
    for(int i = 0; i<p.size(); i++){
        p_.push_back(&p[i]);
        v_.push_back(&v[i]);
    }
    auto newb = zip_to_bodylist(p_,v_,m);
    accelerations(newb, 0.1, 1.0);
    std::cout << *newb[0] << std::endl;
}