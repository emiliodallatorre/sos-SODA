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
            Vector(2, 0, 0),
            Vector(0, 1, 0),
            "blue",
        ),
        Planet(
            "Moon",
            1 / 4,
            Vector(2.01, 0, 0),
            Vector(0, 1, 0),
            "grey",
        ),
    ],
)

dt: float = 1
steps: int = 1000
simulation_results: list = system.simulate(dt, steps)
plotter: Plotter = Plotter(simulation_results, dt, steps)
# plotter.show()
plotter.plot()
