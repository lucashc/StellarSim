#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"


OctNode* accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G) {
    veclist points;
    for (auto body : bodies) {
        points.push_back(&body->pos);
    }
    auto bounds = get_bounding_vectors(points);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first-bounds.second).abs().max();
    std::cout << max_size << std::endl;
    std::vector<OctNode*> leaves;
    auto topnode = new OctNode(center, max_size, bodies, leaves);
    for (auto  leaf : leaves) {
        TreeWalk(topnode, leaf, thetamax, G);
    }
    return topnode;
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
    auto result = accelerations(newb, 0.1, 1.0);
}