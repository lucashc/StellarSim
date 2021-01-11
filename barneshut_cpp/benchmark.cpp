#include <vector>
#include <iostream>
#include "basetypes.hpp"
#include "tree.cpp"
#include "sim.cpp"
#include <assert.h>
#include <cmath>
using namespace std;

int main() {
    auto bl = read_bodylist("seg.bin");
    LeapFrog(bl, 1e-1, 1500, 0.5, 1, 0, 0);
}