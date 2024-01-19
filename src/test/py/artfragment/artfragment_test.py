#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragment class
"""

import unittest
from datetime import timedelta
from commission.artfragment import ArtFragment
from commission.artwork import Artwork
from commission.constraint import Constraint


class TestArtFragment(unittest.TestCase):
    """Test class for ArtFragment class"""

    def setUp(self):
        """Create an instance of ArtFragment based on an Artwork"""
        self.artwork = Artwork(10, 20, timedelta(seconds=0.5))
        constraint = Constraint((-1, 8, 3, 400), "straight")

        self.artwork.set_constraint(constraint)
        self.artfragment = ArtFragment(self.artwork, "1")

    def test_initialization(self):
        """Check if the basic attributes are initialized correctly"""
        self.assertLessEqual(self.artfragment.width, self.artwork.width)
        self.assertLessEqual(self.artfragment.height, self.artwork.height)
        self.assertLessEqual(self.artfragment.coordinates[0], self.artwork.width)
        self.assertLessEqual(self.artfragment.coordinates[1], self.artwork.height)
        print(
            self.artfragment.width,
            self.artfragment.height,
            self.artfragment.coordinates,
        )

    def test_constraint_color_adherence(self):
        """Test the generate_piece method of ArtFragment for color adherence"""
        fragment = self.artfragment.fragment
        color_constraint = self.artwork.get_constraint().color

        for pixel in fragment:
            self.assertEqual(pixel[1], color_constraint)

    def test_pixel_coordinates_adherence(self):
        """Test the generate_piece method of ArtFragment for coordiante adherence"""
        fragment = self.artfragment.fragment
        width_bound = self.artwork.width
        height_bound = self.artwork.height

        for pixel in fragment:
            self.assertLessEqual(pixel[0][0], width_bound)
            self.assertLessEqual(pixel[0][1], height_bound)


if __name__ == "__main__":
    unittest.main()
