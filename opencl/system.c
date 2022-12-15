__kernel void simulate(
        __global const double *masses,
        __global const double *positions_x,
        __global const double *positions_y,
        __global const double *positions_z,
        __global const double *velocities_x,
        __global const double *velocities_y,
        __global const double *velocities_z,
        __global const double *fixed,

        __global double *earth_positions_x,
        __global double *earth_positions_y,
        __global double *earth_positions_z
    )
{
  unsigned int pid = get_global_id(0);

  earth_positions_x[pid] = positions_x[pid];
  earth_positions_y[pid] = positions_y[pid];
  earth_positions_z[pid] = positions_z[pid];

  // Print mass by pid
  printf("pid: %d, mass: %f\n", pid, masses[pid]);
}