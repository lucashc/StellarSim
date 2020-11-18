#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"
#include "sim.cpp"
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
    EulerForward(newb, 20, 20, 0.5, 1);
    std::cout << *newb[0] << std::endl;
}