#include <vector>
#include <iostream>
#include <thread>
#include <cmath>
#include "basetypes.hpp"
#include "progress_bar.hpp"
#include "tree.cpp"


static unsigned int THREAD_COUNT = 4;

static double a_0 = 1.2e-10;
static double r_max = 2.4e+19;
static double rcmw = 9.46073e16;

vec3 dark_matter_gravity(Body body, BASETYPE DM_mass, vec3 center, double G) {
    vec3 r = center - body.pos;
    BASETYPE norm = r.norm2();
    if (norm > 1e10) {
        return r*sqrt(G*DM_mass*a_0)/norm;
    }else {
        return vec3();
    }
}

vec3 pseudo_isothermal_gravity(Body body, BASETYPE DM_mass, vec3 center, double G){
    vec3 dr = center - body.pos;
    if (dr == vec3()) {
        return vec3();
    }
    BASETYPE r = dr.norm();
    BASETYPE norm_const = r_max/rcmw - atan(r_max/rcmw);
    return dr * G*DM_mass/(r*r*r) * (r/rcmw - atan(r/rcmw))/norm_const;
}


void apply_acceleration(int id, bodylist * bodies, OctNode * topnode, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon, BASETYPE DM_mass) {
    for (long unsigned int i = id; i < bodies->size(); i += THREAD_COUNT) {
//        if (i == 0){
//            bodies->at(i)->g = vec3();
//        }else{
//            bodies->at(i)->g = dark_matter_gravity(bodies->at(i), DM_mass, bodies->at(0)->pos, G);
//        }
        bodies->at(i)->g = pseudo_isothermal_gravity(bodies->at(i), DM_mass, bodies->at(0)->pos, G);
        TreeWalk(topnode, bodies->at(i), thetamax, G, epsilon);
    }
}

void accelerated_accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon, BASETYPE DM_mass) {
    auto bounds = get_bounding_vectors(bodies);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first - bounds.second).abs().max();
    auto topnode = new OctNode(center, max_size, bodies);

    std::thread threads[THREAD_COUNT];
    for (unsigned int i = 0; i < THREAD_COUNT; i++){
        threads[i] = std::thread(apply_acceleration, i, &bodies, topnode, thetamax, G, epsilon, DM_mass);
    }

    for (unsigned int i = 0; i < THREAD_COUNT; i++) {
        threads[i].join();
    }
    delete topnode;
}

void accelerations(bodylist &bodies, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon) {
    auto bounds = get_bounding_vectors(bodies);
    auto center = (bounds.first + bounds.second)/2;
    BASETYPE max_size = (bounds.first-bounds.second).abs().max();
    auto topnode = new OctNode(center, max_size, bodies);
    for (auto  b : bodies) {
        b->g = vec3(0,0,0);
        TreeWalk(topnode, b, thetamax, G, epsilon);
    }
    delete topnode;
}


void LeapFrog(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon, BASETYPE DM_mass){
    ProgressBar progress_bar = ProgressBar(n_steps, 100);
    // v0 -> v_{-1/2}
    accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
    for (auto body : bodies) {
        // v_{-1/2} = v_0 - g_0 * 1/2 * dt
        body->vel = body->vel - body->g * 1/2 * dt;
    }
    for(int step = 0; step < n_steps; step++){
        progress_bar.tick();
        accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
        for(auto body : bodies){
            // v_{i+1/2} = v_{i-1/2} + g_i * dt
            body->vel = body->vel + body->g * dt;
            // r_{i+1} = r_i + v_{i+1/2} * dt
            body->pos = body->pos + body->vel * dt;
        }
    }
    progress_bar.tick();
}

bodylist copy_bodylist(bodylist &bodies){
    bodylist copy;
    for(auto b : bodies){
        Body* body_copy = new Body(b);
        copy.push_back(body_copy);
    }
    return copy;
}


std::vector<bodylist> LeapFrogSave(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G, int savestep, BASETYPE epsilon, BASETYPE DM_mass) {
    std::vector<bodylist> save_list;   // save initial state
    ProgressBar progress_bar = ProgressBar(n_steps, 100);
    // v0 -> v_{-1/2}
    accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
    for (auto body : bodies) {
        // v_{-1/2} = v_0 - g_0 * 1/2 * dt
        body->vel = body->vel - body->g * 1/2 * dt;
    }
    for(int step = 0; step < n_steps; step++){
        progress_bar.tick();
        if (step % savestep == 0) {
            save_list.push_back(copy_bodylist(bodies));   // save bodies after a step
        }
        accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
        for(auto body: bodies){
            // v_{i+1/2} = v_{i-1/2} + g_i * dt
            body->vel = body->vel + body->g * dt;
            // r_{i+1} = r_i + v_{i+1/2} * dt
            body->pos = body->pos + body->vel * dt;
        }
    }
    progress_bar.tick();
    return save_list;
}

void ModifiedEuler(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G, BASETYPE epsilon, BASETYPE DM_mass) {
    ProgressBar progress_bar = ProgressBar(n_steps, 100);
    for(int step = 0; step < n_steps; step++){
        progress_bar.tick();
        bodylist forward = copy_bodylist(bodies);
        accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
        for(unsigned int i = 0; i < forward.size(); i++) {
            forward[i]->vel = forward[i]->vel + bodies[i]->g * dt;
            forward[i]->pos = forward[i]->pos + bodies[i]->vel * dt;
        }
        accelerated_accelerations(forward, thetamax, G, epsilon, DM_mass);
        for(unsigned int i = 0; i < forward.size(); i++) {
            bodies[i]->pos = bodies[i]->pos + (bodies[i]->vel + forward[i]->vel)* dt/2;
            bodies[i]->vel = bodies[i]->vel + (bodies[i]->g + forward[i]->g)* dt/2;
        }
    }
    progress_bar.tick();
}

std::vector<bodylist> ModifiedEulerSave(bodylist &bodies, BASETYPE dt, int n_steps, BASETYPE thetamax, BASETYPE G, int savestep, BASETYPE epsilon, BASETYPE DM_mass) {
    std::vector<bodylist> save_list;   // save initial state
    ProgressBar progress_bar = ProgressBar(n_steps, 100);
    for(int step = 0; step < n_steps; step++){
        progress_bar.tick();
        if (step % savestep == 0) {
            save_list.push_back(copy_bodylist(bodies));   // save bodies after a step
        }
        bodylist forward = copy_bodylist(bodies);
        accelerated_accelerations(bodies, thetamax, G, epsilon, DM_mass);
        for(unsigned int i = 0; i < forward.size(); i++) {
            forward[i]->vel = forward[i]->vel + bodies[i]->g * dt;
            forward[i]->pos = forward[i]->pos + bodies[i]->vel * dt;
        }
        accelerated_accelerations(forward, thetamax, G, epsilon, DM_mass);
        for(unsigned int i = 0; i < forward.size(); i++) {
            bodies[i]->pos = bodies[i]->pos + (bodies[i]->vel + forward[i]->vel)* dt/2;
            bodies[i]->vel = bodies[i]->vel + (bodies[i]->g + forward[i]->g)* dt/2;
        }
    }
    progress_bar.tick();
    return save_list;
}