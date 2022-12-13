from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.pyplot import subplots


class Plotter:
    def __init__(self, simulation_results: list, dt: float, steps: int):
        self.simulation_results = simulation_results
        self.dt = dt
        self.steps = steps

        fig, ax = subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            # figsize=(self.size / 50, self.size / 50),
        )

        farthest_x: float = 0
        farthest_y: float = 0
        farthest_z: float = 0

        for planets in self.simulation_results:
            for planet in planets:
                if abs(planet.position.x) > farthest_x:
                    farthest_x = planet.position.x
                if abs(planet.position.y) > farthest_y:
                    farthest_y = planet.position.y
                if abs(planet.position.z) > farthest_z:
                    farthest_z = planet.position.z

        def animate(i):
            ax.clear()

            ax.set_xlim(-farthest_x, farthest_x)
            ax.set_ylim(-farthest_y, farthest_y)
            ax.set_zlim(-farthest_z, farthest_z)

            for planet in self.simulation_results[i]:
                ax.plot(
                    planet.position.x, planet.position.y, planet.position.z,
                    marker="o",
                    markersize=max([planet.mass * 10, 5]),
                    color=planet.color,
                )

                ax.quiver(
                    planet.position.x, planet.position.y, planet.position.z,
                    planet.velocity.x, planet.velocity.y, planet.velocity.z,
                )

                planet.acting_force *= 1
                ax.quiver(
                    planet.position.x, planet.position.y, planet.position.z,
                    planet.acting_force.x, planet.acting_force.y, planet.acting_force.z,
                    color="red",
                )

                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")

        self.animation = FuncAnimation(fig, animate, frames=self.steps,
                                       interval=dt * 1000)

    def plot(self):
        video_file = r"animation.mp4"
        writer = FFMpegWriter(fps=20)
        self.animation.save(video_file, writer=writer)

    def show(self):
        plt.show()
