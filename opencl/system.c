

int access2Darray(int x, int y, int width) {
    return y * width + x;
}

int access3Darray(int x, int y, int z, int width, int height) {
    return z * width * height + y * width + x;
}

double getAcceleration(double mass, double otherMass, double position, double otherPosition, bool fixed) {
    double distance = position - otherPosition;
    if (fixed || fabs(distance) < 0.0001) {
        return 0.0f;
    }

    int direction = distance > 0 ? -1 : 1;

    double acceleration = direction * otherMass / (distance * distance);

    // Print data of the calculation
    // printf("Mass: %f, OtherMass: %f, Position: %f, OtherPosition: %f, Distance: %f, Acceleration: %f\n", mass, otherMass, position, otherPosition, distance, acceleration);

    return acceleration;
}

__kernel void calculateAccelerations(
        __global const double *masses,
        __global const double *fixed,
        __global const double *positions,

        int step,
        int planetCount,
        int dimensionCount,

        __global double *accelerations
) {
    unsigned int planetId = get_global_id(0);
    unsigned int otherPlanetId = get_global_id(1);
    unsigned int dimensionId = get_global_id(2);

    double mass = masses[planetId];
    double otherMass = masses[otherPlanetId];
    double position = positions[access3Darray(dimensionId, planetId, step, dimensionCount, planetCount)];
    double otherPosition = positions[access3Darray(dimensionId, otherPlanetId, step, dimensionCount, planetCount)];
    bool isFixed = fixed[planetId];

    double acceleration = getAcceleration(mass, otherMass, position, otherPosition, isFixed);
    accelerations[access2Darray(dimensionId, planetId, dimensionCount)] = acceleration + accelerations[access2Darray(dimensionId, planetId, dimensionCount)];
}

__kernel void advancePositions(
    __global const double *fixed,
    __global double* positions,
    __global double* velocities,
    __global const double* accelerations,

    const double dt,
    const int time,
    const int planetCount,
    const int dimensionCount
) {
    unsigned int planetId = get_global_id(0);
    unsigned int dimensionId = get_global_id(1);

    // If the planet is fixed, we don't need to calculate anything
    bool isFixed = fixed[planetId];
    if (isFixed) {
        return;
    }

    double position = positions[access3Darray(dimensionId, planetId, time, dimensionCount, planetCount)];

    velocities[access3Darray(dimensionId, planetId, time, dimensionCount, planetCount)] += accelerations[access2Darray(dimensionId, planetId, dimensionCount)] * dt;
    double velocity = velocities[access2Darray(dimensionId, planetId, dimensionCount)];

    double newPosition = position + velocity * dt;
    positions[access3Darray(dimensionId, planetId, time, dimensionCount, planetCount)] = newPosition;
}

