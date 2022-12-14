


__kernel void simulate(
        __global const float *masses_buf,
        __global const float *positions_x_buf,
        __global const float *positions_y_buf,
        __global const float *positions_z_buf,
        __global const float *velocities_x_buf,
        __global const float *velocities_y_buf,
        __global const float *velocities_z_buf,
        __global float *fixed_buf,

        __global float *earth_positions_x_buf,
        __global float *earth_positions_y_buf,
        __global float *earth_positions_z_buf,
    )
{
  int pid = get_global_id(0);

  earth_positions_x_buf[pid] = positions_x_buf[pid];
  earth_positions_y_buf[pid] = positions_y_buf[pid];
  earth_positions_z_buf[pid] = positions_z_buf[pid];
}