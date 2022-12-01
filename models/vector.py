import math


class Vector:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def distance(self, other) -> float:
        return (self - other).length()

    def versor(self) -> 'Vector':
        return self / self.length()
