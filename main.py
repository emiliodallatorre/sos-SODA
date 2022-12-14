from math import sqrt

from models.planet import Planet
from models.system import System
from models.vector import Vector
from plotter import Plotter

system: System = System(
    [
        Planet(
            "Sun",
            1,
            Vector(0, 0, 0),
            Vector(0, 0, 0),
            "yellow",
            True,
        ),
        Planet(
            "Earth",
            1 / 2,
            Vector(4, 0, 0),
            Vector(0, 1 / 2, 0),
            "blue",
        ),
        Planet(
            "Moon",
            1 / 2000,
            Vector(4 + 0.04 * sqrt(2) / 2, 0, 0.04 * sqrt(2) / 2),
            Vector(-5 / sqrt(2) * sqrt(2) / 2, 1 / 2, 5 / sqrt(2) * sqrt(2) / 2),
            "gray",
        ),
    ],
    G=1,
)

dt: float = 0.001
steps: int = 1000
simulation_results: list = system.simulate(dt, steps)
plotter: Plotter = Plotter(simulation_results, dt, steps)

# plotter.static_plot()
# plotter.show()
plotter.plot()
