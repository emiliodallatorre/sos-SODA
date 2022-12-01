from copy import deepcopy

from models.vector import Vector


class System:
    planets: list = []
    states: list = []
    dt: float
    steps: int

    def __init__(self, planets: list):
        self.planets = planets

    def step(self, dt: float):
        for planet in self.planets:
            if planet.fixed:
                continue

            for other in self.planets:
                if other is planet:
                    continue

                distance: float = planet.position.distance(other.position)
                force: Vector = planet.mass * other.mass / (distance ** 2)
                force_direction: Vector = (planet.position - other.position).versor()

                planet.velocity -= force_direction * (force / planet.mass) * dt

        for planet in self.planets:
            planet.position = planet.position + planet.velocity * dt

        self.states.append(deepcopy(self.planets))

    def simulate(self, dt: float, steps: int) -> list:
        self.dt = dt
        self.steps = steps

        for i in range(steps):
            self.step(dt)

        return self.states
