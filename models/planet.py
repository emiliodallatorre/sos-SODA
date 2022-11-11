from models.vector import Vector


class Planet:
    name: str
    mass: float
    position: Vector
    velocity: Vector

    fixed: bool

    def __init__(self, name: str, mass: float, position: Vector, velocity: Vector, fixed: bool = False):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.fixed = fixed
