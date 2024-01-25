#!/usr/bin/env python3

"""
Simple Test Module for the Constraint class
"""

import unittest
from commission.artwork import Constraint
from drawing.color import Color


class TestConstraint(unittest.TestCase):
    """Test class for Constraint class"""

    def setUp(self):
        """Create an instance of Constraint"""
        self.constraint = Constraint(Color(0, 8, 3, 255), "straight")

    def test_initialization(self):
        """Check if the attributes are initialized correctly"""
        self.assertEqual(self.constraint.color.channels, (0, 8, 3, 255))
        self.assertEqual(self.constraint.line_type, "straight")


if __name__ == "__main__":
    unittest.main()
