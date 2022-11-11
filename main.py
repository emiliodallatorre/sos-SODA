from math import sqrt

from models.planet import Planet
from models.system import System
from models.vector import Vector

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
            1,
            Vector(sqrt(2), sqrt(2), 0),
            Vector(0.5, -0.5, 0),
            "blue",
        ),
        Planet(
            "Moon",
            1,
            Vector(sqrt(2.0001), sqrt(2.0001), 0),
            Vector(0.5, -0.5, 0),
            "grey",
        ),
    ],
)

for i in range(2000):
    system.step(0.1)
    if i % 100 == 0:
        print(i)

system.draw_system()
system.save_system("test.png")
