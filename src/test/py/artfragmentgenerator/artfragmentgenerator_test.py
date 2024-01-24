#!/usr/bin/env python3

"""
Simple Test Module for the ArtFragmentGenerator class
"""

import unittest
from datetime import timedelta
from commission.artfragmentgenerator import ArtFragmentGenerator
from commission.artwork import Artwork
from commission.constraint import Constraint
from drawing.color import Color


class TestArtFragmentGenerator(unittest.TestCase):
    """Test class for ArtFragmentGenerator class"""

    def setUp(self):
        """Create an instance of ArtFragmentGenerator based on an Artwork"""
        self.artwork = Artwork(10, 20, timedelta(seconds=0.5))
        constraint = Constraint(Color(-1, 8, 3, 400), "straight")
        self.artwork.set_constraint(constraint)
        self.artfragment_generator = ArtFragmentGenerator()

    def test_generate_subcanvas(self):
        """Test the generate_subcanvas method of ArtFragmentGenerator for bound adherence"""
        artwork = self.artwork
        subcanvas = self.artfragment_generator.generate_subcanvas(
            artwork.width, artwork.height
        )

        x_coordinate = subcanvas[0][0]
        y_coordinate = subcanvas[0][0]
        subcanvas_width = subcanvas[1][0]
        subcanvas_height = subcanvas[1][1]

        width_bound = artwork.width - x_coordinate + 1
        height_bound = artwork.height - y_coordinate + 1

        self.assertLessEqual(x_coordinate, artwork.width)
        self.assertLessEqual(y_coordinate, artwork.height)
        self.assertLessEqual(subcanvas_width, width_bound)
        self.assertLessEqual(subcanvas_height, height_bound)

    def test_generate_pixels(self):
        """
        Test the generate_pixel method of ArtFragmentGenerator for coordinate, color adherence
        """
        artwork = self.artwork
        subcanvas = self.artfragment_generator.generate_subcanvas(
            artwork.width, artwork.height
        )

        pixels = self.artfragment_generator.generate_pixels(
            subcanvas, artwork.get_constraint()
        )
        color_constraint = artwork.get_constraint().get_color()

        for pixel in pixels:
            coordinates = pixel.coordinates
            color = pixel.color
            self.assertLessEqual(coordinates.x, artwork.width)
            self.assertLessEqual(coordinates.y, artwork.height)
            self.assertEqual(color, color_constraint)


if __name__ == "__main__":
    unittest.main()
