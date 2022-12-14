import numpy as np
import pyopencl as cl

from models.system import System


class OpenCLSystem:
    system: System
    initialized: bool = False

    masses: np.array(np.float32)
    positions_x: np.array(np.float32)
    positions_y: np.array(np.float32)
    positions_z: np.array(np.float32)
    velocities_x: np.array(np.float32)
    velocities_y: np.array(np.float32)
    velocities_z: np.array(np.float32)
    fixed: np.array

    context: cl.Context

    def __init__(self, system: System):
        self.masses_buf = None
        self.positions_x_buf = None
        self.positions_y_buf = None
        self.positions_z_buf = None
        self.velocities_x_buf = None
        self.velocities_y_buf = None
        self.velocities_z_buf = None
        self.fixed_buf = None

        self.system = system

        self.masses = np.array([planet.mass for planet in system.planets])
        self.positions_x = np.array([planet.position.x for planet in system.planets])
        self.positions_y = np.array([planet.position.y for planet in system.planets])
        self.positions_z = np.array([planet.position.z for planet in system.planets])
        self.velocities_x = np.array([planet.velocity.x for planet in system.planets])
        self.velocities_y = np.array([planet.velocity.y for planet in system.planets])
        self.velocities_z = np.array([planet.velocity.z for planet in system.planets])
        self.fixed = np.array([planet.fixed for planet in system.planets])

    def initialize(self):
        # Select a device
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)

        # Allocate memory on the device and copy the content of our numpy array
        self.masses_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                    hostbuf=self.masses)
        self.positions_x_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                         hostbuf=self.positions_x)
        self.positions_y_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                         hostbuf=self.positions_y)
        self.positions_z_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                         hostbuf=self.positions_z)
        self.velocities_x_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                          hostbuf=self.velocities_x)
        self.velocities_y_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                          hostbuf=self.velocities_y)
        self.velocities_z_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                          hostbuf=self.velocities_z)
        self.fixed_buf = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                                   hostbuf=self.fixed)

        with open("opencl/system.c", "r") as f:
            kernel = f.read()
        self.opencl_program = cl.Program(self.context, kernel).build()

        self.initialized = True

    def simulate(self, steps: int, dt: float):
        if not self.initialized:
            self.initialize()

        earth_positions_x_buf: cl.Buffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, 8 * steps)
        earth_positions_y_buf: cl.Buffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, 8 * steps)
        earth_positions_z_buf: cl.Buffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, 8 * steps)

        self.opencl_program.simulate(
            self.queue,
            self.opencl_program.simulate,
            steps * 8 * 12,
            None,

            self.masses_buf,
            self.positions_x_buf,
            self.positions_y_buf,
            self.positions_z_buf,
            self.velocities_x_buf,
            self.velocities_y_buf,
            self.velocities_z_buf,
            self.fixed_buf,
            earth_positions_x_buf,
            earth_positions_y_buf,
            earth_positions_z_buf,
        )

        earth_positions_x = np.empty(steps, dtype=np.float32)
        earth_positions_y = np.empty(steps, dtype=np.float32)
        earth_positions_z = np.empty(steps, dtype=np.float32)

        cl.enqueue_copy(self.queue, earth_positions_x, earth_positions_x_buf)
        cl.enqueue_copy(self.queue, earth_positions_y, earth_positions_y_buf)
        cl.enqueue_copy(self.queue, earth_positions_z, earth_positions_z_buf)

        return earth_positions_x, earth_positions_y, earth_positions_z
