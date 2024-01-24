#!/usr/bin/env python3

"""
Simple Test Module for the Coordinates class
"""

import unittest
from random import randrange
from drawing.coordinates import Coordinates


class TestCoordinates(unittest.TestCase):
    """Test class for Coordinates class"""

    def setUp(self):
        """Create an instance of Coordinates"""
        self.coordinates = Coordinates(-19, 9)

    def test_normalize_coordinates(self):
        """Check if coordinates is normalized correctly"""
        self.assertEqual(self.coordinates.x, 0)
        self.assertEqual(self.coordinates.y, 9)

    def test_create_bounds(self):
        """Check if correct bounds are created"""
        width = randrange(1, 11)
        height = randrange(10, 41)
        bounds = self.coordinates.create_bounds(width, height)
        self.assertLessEqual(bounds[0] - 1, width)
        self.assertLessEqual(bounds[1] - 1, height)


if __name__ == "__main__":
    unittest.main()
