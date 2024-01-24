#!/usr/bin/env python3
"""
Module to manage ArtFragmentGenerator

ArtFragmentGenerator class allows us to create an instance of ArtFragment
"""

import logging
from random import randrange
from commission.artwork import Artwork
from commission.constraint import Constraint
from commission.artfragment import ArtFragment
from drawing.pixel import Pixel
from drawing.coordinates import Coordinates


class ArtFragmentGenerator:
    """
    Class to generate ArtFragment
    """

    logger = logging.getLogger("ArtFragmentGenerator")

    def __init__(self):
        """
        Initializes an instance of the ArtFragmentGenerator class.
        """

    def generate_fragment(self, artwork: Artwork, contributor: str):
        """
        Generates a ArtFragment instance
        - artwork (Artwork): Artwork that the ArtFragment is intended for.
        - contributor (str): Peer ID that created the ArtFragment.
        """
        # generate starting (x,y) coordinates and width, height
        subcanvas = self.generate_subcanvas(artwork.width, artwork.height)
        constraint = artwork.get_constraint()

        # generate set of Pixel with color constraint adherence.
        pixels = self.generate_pixels(subcanvas, constraint)

        # generate ArtFragment
        fragment = ArtFragment(artwork, contributor, pixels)
        return fragment

    def generate_subcanvas(self, width: int, height: int):
        """
        Generates starting (x,y) coordinates with width and height adhering to artwork
        """
        x_coordinate = randrange(0, width)
        y_coordinate = randrange(0, height)
        coordinates = Coordinates(x_coordinate, y_coordinate)
        bounds = coordinates.create_bounds(width, height)

        subcanvas_width = randrange(1, bounds[0])
        subcanvas_height = randrange(1, bounds[1])

        return ((x_coordinate, y_coordinate), (subcanvas_width, subcanvas_height))

    def generate_pixels(
        self, subcanvas: tuple[tuple[int, int], tuple[int, int]], constraint: Constraint
    ):
        """
        Generate a list of pixel info that adheres to coordiantes, dimensions, constraints

        TODO:
        - implement address-based adherence
        - implement line type adherence
        """
        coordinates = subcanvas[0]
        dimensions = subcanvas[1]
        color_constraint = constraint.get_color()

        x_coordinate = coordinates[0]
        y_coordinate = coordinates[1]

        width = dimensions[0]
        height = dimensions[1]

        # generate the set of pixels to occupy
        num_pixels = randrange(0, width * height)
        x_bound = x_coordinate + width
        y_bound = y_coordinate + height
        set_pixels = set()

        while num_pixels > 0:
            coordinates = Coordinates(
                randrange(x_coordinate, x_bound), randrange(y_coordinate, y_bound)
            )

            pixel = Pixel(coordinates, color_constraint)
            set_pixels.add(pixel)
            num_pixels -= 1

        return set_pixels
