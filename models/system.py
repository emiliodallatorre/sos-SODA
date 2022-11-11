import matplotlib.pyplot as plt


class System:
    planets: list = []
    fig: plt.Figure
    ax: plt.Axes

    def __init__(self, planets: list, plot_size: tuple = (10, 10)):
        self.planets = planets

    def step(self, dt: float):
        for planet in self.planets:
            if planet.fixed:
                continue

            for other in self.planets:
                if other is planet:
                    continue

                distance = planet.current_position().distance(other.current_position())
                force = planet.mass * other.mass / distance ** 2

                direction = (planet.current_position() - other.current_position()) / distance
        
                planet.velocity += direction * force / planet.mass * dt

            planet.new_position(planet.current_position() + planet.velocity * dt)
