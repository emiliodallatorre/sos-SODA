import matplotlib.pyplot as plt

from models.planet import Planet


class System:
    planets: list = []
    fig: plt.Figure
    ax: plt.Axes

    def __init__(self, planets: list, plot_size: tuple = (10, 10)):
        self.planets = planets

        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=plot_size,
        )
        self.fig.show()

    def step(self, dt: float):
        for planet in self.planets:
            self.draw_planet(planet)

            if planet.fixed:
                continue

            for other in self.planets:
                if other is planet:
                    continue

                distance = planet.position.distance(other.position)
                force = planet.mass * other.mass / distance ** 2

                direction = (other.position - planet.position) / distance

                planet.velocity += direction * force / planet.mass * dt

            planet.position += planet.velocity * dt

        # self.draw_system()

    def draw_planet(self, planet: Planet):
        """
        Draw a planet in the system
        :param planet:
        :return:
        """

        self.ax.scatter(
            planet.position.x,
            planet.position.y,
            planet.position.z,
            color=planet.color,
            s=planet.mass * 100,
        )

    def draw_system(self):
        """
        Draw the system in a 3D plot
        :return:
        """
        #  farthest_planet_distance: float = max(self.planets,
        #                                      key=lambda planet: planet.position.length()).position.length()
        # axes_limit = farthest_planet_distance * 1.1
        # self.ax.set_xlim(-axes_limit, axes_limit)
        # self.ax.set_ylim(-axes_limit, axes_limit)
        # self.ax.set_zlim(-axes_limit, axes_limit)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def save_system(self, filename: str):
        """
        Save the system in a 3D plot
        :return:
        """
        self.fig.savefig(filename)