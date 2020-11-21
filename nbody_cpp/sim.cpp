#include "sim.hpp"

void accelerate(bodylist bodies) {
    for (Body* body1 : bodies) {
        for (Body* body2 : bodies) {
            if (body1 == body2) continue;
            body1->vel += body2->pull(body1->pos);
        }
    }
}

void simulate(bodylist bodies, std::vector<bodylist> data) {
    
}