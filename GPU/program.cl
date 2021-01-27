__kernel void get_accelerations(const int n_bodies, __global const body *bodies, __global double *acc, const double G) {
    int i = get_global_id(0);
    double gx = 0, gy = 0, gz = 0;
    for (int j = 0; j < n_bodies; j++) {
        if (i == j) continue;
        double rx = bodies[j].pos[0]-bodies[i].pos[0];
        double ry = bodies[j].pos[1]-bodies[i].pos[1];
        double rz = bodies[j].pos[2]-bodies[i].pos[2];
        double dr = rsqrt(rx*rx + ry*ry + rz*rz);
        double dr3 = dr * dr * dr;
        gx += G * rx * bodies[j].mass * dr3;
        gy += G * ry * bodies[j].mass * dr3;
        gz += G* rz * bodies[j].mass * dr3;
    }
    acc[i*3 + 0] = gx;
    acc[i*3 + 1] = gy;
    acc[i*3 + 2] = gz;
}

__kernel void update_velocities(int n_bodies, __global body *bodies, double G, double dt) {
    int i = get_global_id(0);
    double gx = 0, gy = 0, gz = 0;
    for (int j = 0; j < n_bodies; j++) {
        if (i == j) continue;
        double rx = bodies[j].pos[0]-bodies[i].pos[0];
        double ry = bodies[j].pos[1]-bodies[i].pos[1];
        double rz = bodies[j].pos[2]-bodies[i].pos[2];
        double dr = sqrt(rx*rx + ry*ry + rz*rz);
        double dr3 = dr * dr * dr;
        gx += G * rx * bodies[j].mass / dr3;
        gy += G * ry * bodies[j].mass / dr3;
        gz += G * rz * bodies[j].mass / dr3;
    }
    bodies[i].vel[0] += gx*dt;
    bodies[i].vel[1] += gy*dt;
    bodies[i].vel[2] += gz*dt;
}

__kernel void update_positions(__global body *bodies, const double dt) {
    int i = get_global_id(0);
    bodies[i].pos[0] += bodies[i].vel[0]*dt;
    bodies[i].pos[1] += bodies[i].vel[1]*dt;
    bodies[i].pos[2] += bodies[i].vel[2]*dt;
}

__kernel void update(int n_bodies, __global body *bodies, double G, double dt) {
    int i = get_global_id(0);
    double gx = 0, gy = 0, gz = 0;
    for (int j = 0; j < n_bodies; j++) {
        if (i == j) continue;
        double rx = bodies[j].pos[0]-bodies[i].pos[0];
        double ry = bodies[j].pos[1]-bodies[i].pos[1];
        double rz = bodies[j].pos[2]-bodies[i].pos[2];
        double dr = sqrt(rx*rx + ry*ry + rz*rz);
        double dr3 = dr * dr * dr;
        gx += G * rx * bodies[j].mass / dr3;
        gy += G * ry * bodies[j].mass / dr3;
        gz += G * rz * bodies[j].mass / dr3;
    }
    bodies[i].vel[0] += gx*dt;
    bodies[i].vel[1] += gy*dt;
    bodies[i].vel[2] += gz*dt;
    bodies[i].pos[0] += bodies[i].vel[0]*dt;
    bodies[i].pos[1] += bodies[i].vel[1]*dt;
    bodies[i].pos[2] += bodies[i].vel[2]*dt;
}