#include <vector>
#include <iostream>
#include "../basetypes.hpp"
#include "../tree.cpp"
#include "../sim.cpp"
#include <assert.h>
#include <cmath>
using namespace std;

int main() {

    auto b1 = Body(vec3(10, 10, 10), vec3(1, -1, 1), 10);
    auto b2 = Body(vec3(10, -10, 10), vec3(1, -1, 1), 10);
    auto b3 = Body(vec3(10, 10, -10), vec3(1, -1, 1), 10);
    auto b4 = Body(vec3(10, 12, 10), vec3(1, -1, 1), 10);
    auto b5 = Body(vec3(11, 10, 10), vec3(1, -1, 1), 10);
    auto b6 = Body(vec3(10, 10, -11), vec3(1, -1, 1), 10);
    auto b7 = Body(vec3(10, 13, 10), vec3(1, -1, 1), 10);
    auto b8 = Body(vec3(-10, -10, 10), vec3(1, -1, 1), 10);

    bodylist bl = bodylist({&b1, &b2, &b3, &b4, &b5, &b6, &b7, &b8});

    cout << "Starting LeapFrog" << endl;
    LeapFrog(bl, 1, 1000, 1, 0.1, 0.1, 100);


}