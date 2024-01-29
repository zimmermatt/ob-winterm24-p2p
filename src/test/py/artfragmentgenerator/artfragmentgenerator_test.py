#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragmentGenerator class
"""

import unittest
from unittest.mock import Mock
from datetime import timedelta
from commission.artfragmentgenerator import generate_subcanvas, generate_pixels
from commission.artwork import Artwork
from commission.artwork import Constraint
from drawing.color import Color


class TestArtFragmentGenerator(unittest.TestCase):
    """Test class for ArtFragmentGenerator class"""

    def setUp(self):
        """Create an instance of ArtFragmentGenerator based on an Artwork"""
        constraint = Constraint(Color(0, 8, 3, 255), "straight")
        self.artwork = Artwork(
            10, 20, timedelta(seconds=0.5), Mock(), constraint=constraint
        )

    def test_generate_subcanvas(self):
        """Test the generate_subcanvas method of ArtFragmentGenerator for bound adherence"""
        artwork = self.artwork
        subcanvas = generate_subcanvas(artwork.width, artwork.height)

        x_coordinate = subcanvas.coordinates.x
        y_coordinate = subcanvas.coordinates.y
        subcanvas_width = subcanvas.dimensions[0]
        subcanvas_height = subcanvas.dimensions[1]

        width_bound = artwork.width - x_coordinate + 1
        height_bound = artwork.height - y_coordinate + 1

        self.assertLess(x_coordinate, artwork.width)
        self.assertLess(y_coordinate, artwork.height)
        self.assertLessEqual(subcanvas_width, width_bound)
        self.assertLessEqual(subcanvas_height, height_bound)

    def test_generate_pixels(self):
        """
        Test the generate_pixel method of ArtFragmentGenerator for coordinate, color adherence
        """
        artwork = self.artwork
        subcanvas = generate_subcanvas(artwork.width, artwork.height)

        pixels = generate_pixels(subcanvas, artwork.constraint)
        color_constraint = artwork.constraint.color

        for pixel in pixels:
            coordinates = pixel.coordinates
            color = pixel.color
            self.assertLess(coordinates.x, artwork.width)
            self.assertLess(coordinates.y, artwork.height)
            self.assertEqual(color, color_constraint)


if __name__ == "__main__":
    unittest.main()
