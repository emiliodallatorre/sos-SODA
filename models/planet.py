from models.vector import Vector


class Planet:
    name: str
    mass: float
    positions: list
    velocity: Vector
    color: str

    fixed: bool

    def __init__(self, name: str, mass: float, position: Vector, velocity: Vector, color: str, fixed: bool = False):
        self.name = name
        self.mass = mass
        self.positions = [position]
        self.velocity = velocity
        self.color = color
        self.fixed = fixed

    def current_position(self) -> Vector:
        return self.positions[-1]

    def new_position(self, position: Vector):
        self.positions.append(position)
