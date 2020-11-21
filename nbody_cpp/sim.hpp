#ifndef SIM
#define SIM
#include <vector>
#include "body.cpp"

void accelerate(bodylist&);
void simulate(bodylist, std::vector<bodylist>);

#endif