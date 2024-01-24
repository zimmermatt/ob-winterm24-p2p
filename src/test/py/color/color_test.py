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
        self.color = Color(-1, 8, 3, 400)

    def test_normalize_color(self):
        """Check if color is normalized correctly"""
        self.assertEqual(self.color.get_channels(), (0, 8, 3, 255))


if __name__ == "__main__":
    unittest.main()
