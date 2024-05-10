#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragmentGenerator class
"""

import unittest
from unittest.mock import Mock
from datetime import timedelta
from commission.artfragmentgenerator import (
    generate_subcanvas,
    generate_pixels,
    get_bounds,
)
from commission.artwork import Artwork
from drawing.drawing import Color, Constraint, Coordinates


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

        width_bound = artwork.width - x_coordinate
        height_bound = artwork.height - y_coordinate

        self.assertLess(x_coordinate, artwork.width)
        self.assertLess(y_coordinate, artwork.height)
        self.assertLessEqual(subcanvas_width, width_bound)
        self.assertLessEqual(subcanvas_height, height_bound)

    def test_get_bounds(self):
        """Test get_bounds method for bound adherence"""
        width = 1000
        height = 500
        coordinates = Coordinates(999, 499)
        bounds = get_bounds(coordinates, width, height)
        self.assertEqual(bounds[0], 1)
        self.assertEqual(bounds[1], 1)

        coordinates = Coordinates(0, 0)
        bounds = get_bounds(coordinates, width, height)
        self.assertEqual(bounds[0], 1000)
        self.assertEqual(bounds[1], 500)

        coordinates = Coordinates(1000, 500)
        bounds = get_bounds(coordinates, width, height)
        self.assertEqual(bounds[0], 0)
        self.assertEqual(bounds[1], 0)

    def test_generate_pixels_random_constraint(self):
        """
        Test the generate_pixel method of ArtFragmentGenerator for coordinate, color adherence
        """
        artwork = self.artwork
        subcanvas = generate_subcanvas(artwork.width, artwork.height)

        pixels = generate_pixels(1, 2, subcanvas)

        for pixel in pixels:
            coordinates = pixel.coordinates
            self.assertLess(coordinates.x, artwork.width)
            self.assertLess(coordinates.y, artwork.height)

    def test_generate_pixels_defined_constraint(self):
        """
        Test the generate_pixel method of ArtFragmentGenerator for coordinate, color adherence
        """
        artwork = self.artwork
        subcanvas = generate_subcanvas(artwork.width, artwork.height)
        constraint = Constraint(5, "any")

        pixels = generate_pixels(1, 2, subcanvas, constraint)

        for pixel in pixels:
            coordinates = pixel.coordinates
            self.assertLess(coordinates.x, artwork.width)
            self.assertLess(coordinates.y, artwork.height)


if __name__ == "__main__":
    unittest.main()
