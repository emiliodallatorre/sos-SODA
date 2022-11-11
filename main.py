import matplotlib.pyplot as plt

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
            1 / 2,
            Vector(2, 1, 0),
            Vector(0, 1, 0),
            "blue",
        ),
    ],
)

for i in range(200000):
    system.step(0.1)
    if i % 100 == 0:
        print(f"Step {i}")

fig, ax = plt.subplots(
    1,
    1,
    # subplot_kw=dict(projection="3d"),
    figsize=(10, 10),
)
fig.show()

for planet in system.planets:
    ax.scatter(
        [position.x for position in planet.positions],
        [position.y for position in planet.positions],
        color=planet.color,
        s=planet.mass * 10,
    )

fig.canvas.draw()
fig.canvas.flush_events()
fig.show()
# fig.savefig("test.png")
