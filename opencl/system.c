int access2Darray(int x, int y, int width) {
    return y * width + x;
}

int access3Darray(int x, int y, int z, int width, int height) {
    return z * width * height + y * width + x;
}

double getAcceleration(double mass, double otherMass, double position, double otherPosition, bool fixed) {
    double distance = position - otherPosition;
    if (fixed || distance == 0) {
        return 0.0f;
    }

    int direction = distance > 0 ? -1 : 1;

    double acceleration = direction * otherMass / (distance * distance);

    // Print data of the calculation
    // printf("Mass: %f, OtherMass: %f, Position: %f, OtherPosition: %f, Distance: %f, Acceleration: %f\n", mass, otherMass, position, otherPosition, distance, acceleration);

    return acceleration;
}

__kernel void simulate(
        __global const double *masses,
        __global const double *fixed,
        __global const double *positions,
        __global const double *velocities,

        int planetCount,
        int dimensionCount,

        __global double *accelerations
) {
    unsigned int planetId = get_global_id(0);
    unsigned int otherPlanetId = get_global_id(1);
    unsigned int dimensionId = get_global_id(2);

    uintptr_t planetCountCasted = (uintptr_t) planetCount;
    // uintptr_t dimensionCountCasted = (uintptr_t) dimensionCount;

    double mass = masses[planetId];
    double otherMass = masses[otherPlanetId];
    double position = positions[access2Darray(planetId, dimensionId, planetCountCasted)];
    double otherPosition = positions[access2Darray(otherPlanetId, dimensionId, planetCountCasted)];
    bool isFixed = fixed[planetId];

    // Print if fixed
    // printf("PlanetId: %d, OtherPlanetId: %d, DimensionId: %d, IsFixed: %d\n", planetId, otherPlanetId, dimensionId, isFixed);
    // Print planetId and mass

    if (planetId != otherPlanetId) {
        double acceleration = getAcceleration(mass, otherMass, position, otherPosition, isFixed);
        accelerations[access2Darray(planetId, dimensionId, planetCount)] = acceleration + accelerations[access2Darray(planetId, dimensionId, planetCount)];
        // printf("Planet %d, other planet %d, dimension %d, acceleration %f\n", planetId, otherPlanetId, dimensionId, acceleration);
    }
}


