#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragment class
"""

import unittest
from unittest.mock import Mock
from datetime import timedelta
from commission.artfragmentgenerator import generate_fragment
from commission.artwork import Artwork
from drawing.drawing import Constraint, Pixel


class TestArtFragment(unittest.TestCase):
    """Test class for ArtFragment class"""

    def setUp(self):
        """Create an instance of ArtFragment based on an Artwork"""
        constraint = Constraint(5, "any")
        self.artwork = Artwork(
            10, 20, timedelta(seconds=0.5), Mock(), constraint=constraint
        )
        self.artfragment = generate_fragment(self.artwork, 2, "1", 1)

    def test_initialization(self):
        """Check if the basic attributes are initialized correctly"""
        self.assertEqual(self.artfragment.contributor_id, "1")
        self.assertIsInstance(self.artfragment.pixels, set)
        for pixel in self.artfragment.pixels:
            self.assertIsInstance(pixel, Pixel)


if __name__ == "__main__":
    unittest.main()
