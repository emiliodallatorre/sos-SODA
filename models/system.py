from copy import deepcopy

from models.vector import Vector


class System:
    planets: list = []
    states: list = []
    dt: float
    steps: int

    def __init__(self, planets: list, G=10):
        self.planets = planets
        self.G = G
        self.states.append(deepcopy(self.planets))

    def step(self, dt: float):
        for planet in self.planets:
            if planet.fixed:
                continue

            planet.acting_force = Vector(0, 0, 0)
            for other in self.planets:

                if other is planet:
                    continue

                distance: float = planet.position.distance(other.position)
                force: Vector = self.G * (planet.mass * other.mass) / (distance ** 2)
                force_direction: Vector = (other.position - planet.position).versor()

                planet.velocity += force_direction * (force / planet.mass) * dt
                planet.acting_force += force_direction * force

        for planet in self.planets:
            planet.position = planet.position + (planet.velocity * dt)

        self.states.append(deepcopy(self.planets))

    def simulate(self, dt: float, steps: int) -> list:
        self.states: list = [self.states[0]]

        self.dt = dt
        self.steps = steps

        for i in range(steps):
            self.step(dt)

        return self.states

    def simulate_with_opencl(self, dt: float, steps: int) -> list:
        self.states: list = [self.states[0]]

        from opencl.opencl_system import OpenCLSystem
        opencl_system: OpenCLSystem = OpenCLSystem(self)

        print(opencl_system.simulate(steps, dt))
