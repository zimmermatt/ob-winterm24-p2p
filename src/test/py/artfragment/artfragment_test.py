#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragment class
"""

import unittest
from datetime import timedelta
from commission.artfragmentgenerator import ArtFragmentGenerator
from commission.artwork import Artwork
from commission.constraint import Constraint
from drawing.pixel import Pixel
from drawing.color import Color


class TestArtFragment(unittest.TestCase):
    """Test class for ArtFragment class"""

    def setUp(self):
        """Create an instance of ArtFragment based on an Artwork"""
        self.artwork = Artwork(10, 20, timedelta(seconds=0.5))
        constraint = Constraint(Color(-1, 8, 3, 400), "straight")
        self.artwork.set_constraint(constraint)
        self.artfragment_generator = ArtFragmentGenerator()
        self.artfragment = self.artfragment_generator.generate_fragment(
            self.artwork, "1"
        )

    def test_initialization(self):
        """Check if the basic attributes are initialized correctly"""
        self.assertEqual(self.artfragment.contributor, "1")
        self.assertIsInstance(self.artfragment.pixels, set)
        for pixel in self.artfragment.pixels:
            self.assertIsInstance(pixel, Pixel)


if __name__ == "__main__":
    unittest.main()
