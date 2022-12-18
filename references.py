from math import sqrt

from models.planet import Planet
from models.vector import Vector

planets: list = [
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
]

dots: list = [
    Planet(
        "Random1",
        1 / 2,
        Vector(4, 0, 0),
        Vector(0, 0, 0),
        "blue",
    ),
    Planet(
        "Random2",
        1 / 2,
        Vector(0, -4, 0),
        Vector(0, 0, 0),
        "red",
    ),
    Planet(
        "Random3",
        1 / 2,
        Vector(0, 0, 4),
        Vector(0, 0, 0),
        "green",
    ),
]
