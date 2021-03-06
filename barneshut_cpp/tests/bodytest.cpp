#include <vector>
#include <iostream>
#include "../basetypes.hpp"
#include "../tree.cpp"
#include "../sim.cpp"
#include <assert.h>
#include <cmath>
using namespace std;

int main() {
    // Check Constructors
    auto pos = vec3(1,2,3);
    auto vel = vec3(0,2,4);
    auto g = vec3(-2,-3,-8);
    auto b = Body(pos, vel,10);
    auto b2 = Body(pos, vel, 10, g);
    auto b3 = Body();
    auto b4 = Body(&b);
    assert(b4.pos == b.pos);
    assert(b2.pos == b.pos);
    bodylist bl = bodylist({&b, &b2, &b3, &b4});
    save_bodylist(bl, "test.bin");
    bodylist bk;
    bk = read_bodylist("test.bin");
    assert(bk[0]->pos == b.pos);
    assert(bk[1]->pos == b2.pos);
    assert(bk[2]->pos == b3.pos);
    assert(bk[3]->pos == b4.pos);
}