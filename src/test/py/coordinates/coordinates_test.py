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
        self.coordinates = Coordinates(0, 9)

    def test_check_coordinates(self):
        """Check if coordinates is normalized correctly"""
        with self.assertRaises(Exception):
            self.coordinates.check_coordinate(-1)

    def test_create_bounds(self):
        """Check if correct bounds are created"""
        width = randrange(3, 11)
        height = randrange(3, 41)
        bounds = self.coordinates.create_bounds(width, height)
        self.assertLessEqual(bounds[0] - 1, width)
        self.assertLessEqual(bounds[1] - 1, height)

        # edge cases
        zero_coordinates = Coordinates(0, 0)
        bounds = zero_coordinates.create_bounds(width, height)
        self.assertLessEqual(bounds[0] - 1, width)
        self.assertLessEqual(bounds[1] - 1, height)

        last_pixel_coordinates = Coordinates(width - 1, height - 1)
        bounds = last_pixel_coordinates.create_bounds(width, height)
        self.assertLessEqual(bounds[0] - 1, width)
        self.assertLessEqual(bounds[1] - 1, height)

        next_to_last_pixel_coordinates = Coordinates(width - 2, height - 2)
        bounds = next_to_last_pixel_coordinates.create_bounds(width, height)
        self.assertLessEqual(bounds[0] - 1, width)
        self.assertLessEqual(bounds[1] - 1, height)


if __name__ == "__main__":
    unittest.main()
