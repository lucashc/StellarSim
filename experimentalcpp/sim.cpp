#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"


std::vector<OctNode*> accelerations(bodylist &bodies, float thetamax, float G) {
    veclist points;
    for (auto body : bodies) {
        points.push_back(&body->pos);
    }
    auto bounds = get_bounding_vectors(points);
    auto center = (bounds.first + bounds.second)/2;
    float max_size = (bounds.first-bounds.second).abs().max();
    std::cout << max_size << std::endl;
    std::vector<OctNode*> leaves;
    auto topnode = OctNode(center, max_size, bodies, leaves);
    return leaves;
}

using namespace std;

int main() {
    auto p = veclist { &vec3(0, 0, 0), &vec3(2, 1, 0), &vec3(-1, -1, 0), &vec3(0, 2, 1) };
    auto m = scalist({100.0, 1.0, 2.0, 60.0});
    auto v = veclist{ &vec3(0, 0, 0), &vec3(0, 0, 0), &vec3(0, 0, 0), &vec3(0, 0, 0) };
    auto newb = zip_to_bodylist(p,v,m);
    auto result = accelerations(newb, 0.1, 1.0);
    for (auto c : result) {
        //
    }
}