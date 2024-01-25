#!/usr/bin/env python3

"""
Simple Test Module for the Color class
"""

import unittest
from drawing.color import Color


class TestColor(unittest.TestCase):
    """Test class for Color class"""

    def setUp(self):
        """Create an instance of Color"""
        self.color = Color(0, 8, 3, 255)

    def test_check_color(self):
        """Check if color is checked correctly"""
        with self.assertRaises(Exception):
            self.color.check_color([-1, 8, 3, 255])
        with self.assertRaises(Exception):
            self.color.check_color([0, 8, 3, 400])


if __name__ == "__main__":
    unittest.main()
