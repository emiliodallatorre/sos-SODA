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
            True,
        ),
        Planet(
            "Earth",
            1,
            Vector(1, 1, 0),
            Vector(1, 0, 0),
        ),
    ],
)

while True:
    system.step(0.1)
    system.draw_system()
