#include <vector>
#include <iostream>
#include "../basetypes.hpp"
#include "../tree.cpp"
#include "../sim.cpp"
using namespace std;

int main() {
    //auto p = vector<vec3> {vec3(0, 0, 0), vec3(2, 1, 0), vec3(-1, -1, 0), vec3(0, 2, 1) };
    //auto m = scalist({100.0, 1.0, 2.0, 123456});
    //auto v = vector<vec3>{vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0) };
    auto newb = read_bodylist("galaxies.bin");
    auto s = LeapFrogSave(newb, 1e-2, 3000, 0.5, 1);
    for (auto bl : s) {
        for (auto b : bl) {
            delete b;
        }
    }
    for (auto b : newb) {
        delete b;
    }
}