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
    auto v = vector<vec3> {vec3(0,0,0), vec3(0,100,50), vec3(-100,0,20), vec3(-10,30,0)};
    auto m = scalist({1e6, 1, 1e4, 10});
    veclist p_, v_;
    for(long unsigned int i = 0; i < p.size(); i++){
        p_.push_back(&p[i]);
        v_.push_back(&v[i]);
    }
    auto newb = zip_to_bodylist(p_,v_,m);
    EulerForward(newb, 1, 20, 0.5, 1);
    std::cout << *newb[0] << std::endl;
}