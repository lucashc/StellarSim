#include <vector>
#include <iostream>
#include "../basetypes.hpp"
#include "../tree.cpp"
#include "../sim.cpp"
#include <assert.h>
#include <cmath>
using namespace std;

int main() {
    auto p = vector<vec3> {vec3(0,0,0), vec3(1,2,3)};
    assert((p[0]+p[1]).x == 1);
    assert((p[0]+p[1]).y == 2);
    assert((p[0]+p[1]).z == 3);
    assert((p[0]-p[1]).x==-1);
    assert((p[0]-p[1]).y==-2);
    assert((p[0]-p[1]).z==-3);
    assert(p[1].norm2() == 14);
    assert((p[1]*2).x==2);
    assert((p[1]*2).y==4);
    assert((p[1]*2).z==6);
    assert(p[1].sum() == 6);
    assert(p[1].norm() == sqrt(p[1].norm2()));
    assert(p[1].max() == 3);
    p[1] += p[1]*2;
    assert(p[1].x == 3);
    assert(p[1].y==6);
    assert(p[1].z==9);
    assert(p[1] == vec3(3,6,9));
    cout << p[1] << endl;
}