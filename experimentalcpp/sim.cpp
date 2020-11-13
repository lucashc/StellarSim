#include "tree.cpp"
#include "defs.hpp"
#include <iostream>
#include <vector>

std::vector<OctNode*> accelerations(veclist &points, scalist &masses, float thetamax, float G) {
    auto bounds = get_bounding_vectors(points);
    auto center = (bounds.first + bounds.second)/2;
    float max_size = (bounds.first-bounds.second).abs().max();
    std::cout << max_size << std::endl;
    std::vector<OctNode*> leaves;
    auto topnode = OctNode(center, max_size, masses, points, leaves);
    return leaves;
}

using namespace std;

int main() {
    auto p = std::vector<vec3>({vec3(0.0,0,0), vec3(2,1,0), vec3(-1, -1, 0), vec3(0, 2, 1)});
    auto m = std::vector<float>({100.0, 1.0, 2.0});
    veclist newp;
    scalist newm;
    for (int i = 0; i < p.size(); i++) {
        newp.push_back(&p[i]);
        newm.push_back(&m[i]);
    };
    auto result = accelerations(newp, newm, 0.1, 1.0);
    for (auto c : result) {
        //
    }
}