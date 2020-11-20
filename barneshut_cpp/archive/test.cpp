#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"
#include "sim.cpp"
using namespace std;

int main() {
    //auto p = vector<vec3> {vec3(0, 0, 0), vec3(2, 1, 0), vec3(-1, -1, 0), vec3(0, 2, 1) };
    //auto m = scalist({100.0, 1.0, 2.0, 123456});
    //auto v = vector<vec3>{vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0) };
    auto p = vector<vec3> {vec3(0,0,0), vec3(50,0,0), vec3(0,50,0), vec3(-100,-100,0)};
    auto v = vector<vec3> {vec3(0,0,0), vec3(0,10,5), vec3(-10,0,2), vec3(-1,3,0)};
    auto m = scalist({1e6, 1, 1e4, 10});
    veclist p_, v_;
    for(long unsigned int i = 0; i < p.size(); i++){
        p_.push_back(&p[i]);
        v_.push_back(&v[i]);
    }
    auto newb = zip_to_bodylist(p_,v_,m);
    auto s = EulerForwardSave(newb, 1e-4, 2500, 0.5, 1);
    std::cout << s.size() << std::endl;
    std::cout << *s[2500][0] << std::endl;
    std::cout << *s[2500][1] << std::endl;
    std::cout << *s[2500][2] << std::endl;
    std::cout << *s[2500][3] << std::endl;
    for (auto bl : s) {
        for (auto b : bl) {
            delete b;
        }
    }
    for (auto b : newb) {
        delete b;
    }
}