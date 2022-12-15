import numpy as np
import pyopencl as cl
import pyopencl.array as pycl_array

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
        self.queue = None
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

        print(self.positions_x)

    def initialize(self):
        # Select a device
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)

        # Allocate memory on the device and copy the content of our numpy array
        self.masses = pycl_array.to_device(self.queue, self.masses)
        self.positions_x = pycl_array.to_device(self.queue, self.positions_x)
        self.positions_y = pycl_array.to_device(self.queue, self.positions_y)
        self.positions_z = pycl_array.to_device(self.queue, self.positions_z)
        self.velocities_x = pycl_array.to_device(self.queue, self.velocities_x)
        self.velocities_y = pycl_array.to_device(self.queue, self.velocities_y)
        self.velocities_z = pycl_array.to_device(self.queue, self.velocities_z)
        self.fixed = pycl_array.to_device(self.queue, self.fixed)

        with open("opencl/system.c", "r") as f:
            kernel = f.read()
        self.opencl_program = cl.Program(self.context, kernel).build()

        self.initialized = True

    def simulate(self, steps: int, dt: float):
        if not self.initialized:
            self.initialize()

        earth_positions_x = pycl_array.empty(self.queue, self.positions_x.shape, self.positions_x.dtype)
        earth_positions_y = pycl_array.empty(self.queue, self.positions_y.shape, self.positions_y.dtype)
        earth_positions_z = pycl_array.empty(self.queue, self.positions_z.shape, self.positions_z.dtype)

        self.opencl_program.simulate(
            self.queue,
            (
                len(self.system.planets),
            ),
            None,

            self.masses.data,
            self.positions_x.data,
            self.positions_y.data,
            self.positions_z.data,
            self.velocities_x.data,
            self.velocities_y.data,
            self.velocities_z.data,
            self.fixed.data,

            earth_positions_x.data,
            earth_positions_y.data,
            earth_positions_z.data,
        )

        return [list(earth_positions_x), list(earth_positions_y), list(earth_positions_z)]
