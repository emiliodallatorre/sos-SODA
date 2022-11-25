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
    ],
)

simulation_results: list = system.simulate(10, 100000)

plotter: Plotter = Plotter(simulation_results)
plotter.plot()
