import numpy as np
import pyopencl as cl
import pyopencl.array as pycl_array

from models.system import System

dimensions: int = 3


class OpenCLSystem:
    system: System
    initialized: bool = False

    masses: np.array(np.float64)
    fixed: np.array(np.int32)

    context: cl.Context

    def __init__(self, system: System):
        self.opencl_program = None
        self.accelerations = None
        self.queue = None
        self.system = system

        self.masses = np.array([planet.mass for planet in system.planets])
        self.fixed = np.array([1 if planet.fixed else 0 for planet in system.planets])
        self.positions = np.array(
            [[planet.position.x, planet.position.y, planet.position.z] for planet in system.planets])
        self.velocities = np.array(
            [[planet.velocity.x, planet.velocity.y, planet.velocity.z] for planet in system.planets])

    def initialize(self):
        # Select a device
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)

        # Allocate memory on the device and copy the content of our numpy array
        self.masses = pycl_array.to_device(self.queue, self.masses)
        self.fixed = pycl_array.to_device(self.queue, self.fixed)
        self.positions = pycl_array.to_device(self.queue, self.positions.flatten())
        self.velocities = pycl_array.to_device(self.queue, self.velocities.flatten())
        self.accelerations = pycl_array.empty(self.queue, len(self.system.planets) * dimensions, dtype=np.float64)

        with open("opencl/system.c", "r") as f:
            kernel = f.read()
        self.opencl_program = cl.Program(self.context, kernel).build()

        self.initialized = True

    def simulate(self, steps: int, dt: float):
        if not self.initialized:
            self.initialize()

        self.opencl_program.simulate(
            self.queue,
            (
                len(self.system.planets),
                len(self.system.planets),
                dimensions,
            ),
            None,

            # Constants
            self.masses.data,
            self.fixed.data,
            self.positions.data,
            self.velocities.data,

            # Support
            np.int32(len(self.system.planets)),
            np.int32(dimensions),

            # Results
            self.accelerations.data,
        )


        print(self.accelerations.reshape((len(self.system.planets), dimensions)))

        return
