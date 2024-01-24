#!/usr/bin/env python3

"""
Simple Test Module for the Pixel class
"""

import unittest
from drawing.pixel import Pixel
from drawing.coordinates import Coordinates
from drawing.color import Color


class TestPixel(unittest.TestCase):
    """Test class for Pixel class"""

    def setUp(self):
        """Create an instance of Pixel"""
        self.color = Color(-1, 8, 3, 400)
        self.coordinates = Coordinates(-19, 9)
        self.pixel = Pixel(self.coordinates, self.color)

    def test_initialization(self):
        """Check if pixel is initialized correctly"""
        self.assertEqual(self.pixel.get_color(), self.color)
        self.assertEqual(self.pixel.get_coordinates(), self.coordinates)


if __name__ == "__main__":
    unittest.main()
