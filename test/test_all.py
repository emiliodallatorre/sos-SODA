import math
import unittest

from models.vector import Vector


class VectorTestCase(unittest.TestCase):
    def test_multiplication_by_scalar(self):
        vector = Vector(1, 2, 3)
        vector *= 2
        self.assertEqual(vector.x, 2)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 6)

    def test_division_by_scalar(self):
        vector = Vector(2, 4, 6)
        vector /= 2
        self.assertEqual(vector.x, 1)
        self.assertEqual(vector.y, 2)
        self.assertEqual(vector.z, 3)

    def test_addition(self):
        vector = Vector(1, 2, 3)
        vector += Vector(1, 2, 3)
        self.assertEqual(vector.x, 2)
        self.assertEqual(vector.y, 4)
        self.assertEqual(vector.z, 6)

    def test_subtraction(self):
        vector = Vector(2, 4, 6)
        vector -= Vector(1, 2, 3)
        self.assertEqual(vector.x, 1)
        self.assertEqual(vector.y, 2)
        self.assertEqual(vector.z, 3)

    def test_length(self):
        vector = Vector(3, 4, 5)
        self.assertEqual(vector.length(), math.sqrt(50))

    def test_distance(self):
        vector = Vector(3, 4, 5)
        self.assertEqual(vector.distance(Vector(0, 0, 0)), math.sqrt(50))


if __name__ == '__main__':
    unittest.main()
