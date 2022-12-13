from models.vector import Vector


class Planet:
    name: str
    mass: float
    position: Vector
    velocity: Vector
    acceleration: Vector = Vector(0, 0, 0)
    acting_force: Vector = Vector(0, 0, 0)
    color: str

    fixed: bool

    def __init__(self, name: str, mass: float, position: Vector, velocity: Vector, color: str, fixed: bool = False):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.color = color
        self.fixed = fixed
