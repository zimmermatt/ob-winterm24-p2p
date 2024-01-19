#!/usr/bin/env python3
"""
Module to manage artfragment commission class

ArtFragment class allows us to create a piece designated for an artwork"""
from random import randrange
import logging
from commission.artwork import Artwork

class ArtFragment:
    """
    Class to manage artfragment commissions
    """
    logger = logging.getLogger("ArtFragment")

    def __init__(self, artwork: Artwork, contributor):
        """
        Initializes an instance of the artfragment class.
        - width (float): The width of the artfragment.
        - height (float): The height of the artfragment.
        - coordinates (tuple): (x,y) coordinate of the artfragment.
        - contributor (string): Peer ID that created the artfragment.
        - artwork (Artwork): artwork that the fragment is intended for.
        - fragment (set): list of (x,y,color) based on constraint.
        """
        self.width = 0
        self.height = 0
        self.coordinates = ()
        self.contributor = contributor
        self.artwork = artwork
        self.fragment = self.generate_piece(artwork)

    def check_valid_piece(self, artwork):
        """
        Checks whether the piece is valid against the art work. Exceptions:
        - width, height or coordinates go out of bounds of artwork
        """
        if (self.width + self.coordinates[0]) > self.artwork.width or (self.height + self.coordinates[1]) > self.artwork.height:
            return False
        return True

    def generate_piece(self, artwork: Artwork):
        """
        Generates a set of pixels to occupy based on artwork
        """
        # generate (x,y) coordinates and width, height
        x_coordinate = randrange(0, artwork.width + 1)
        y_coordinate = randrange(0, artwork.height + 1)
        width = randrange(x_coordinate, artwork.width + 1) - x_coordinate
        height = randrange(y_coordinate, artwork.height + 1) - y_coordinate

        self.coordinates = (x_coordinate, y_coordinate)
        self.width = width
        self.height = height

        self.logger.info("(x,y) coordinates: %s, (width, height): %s", (x_coordinate,y_coordinate), (width, height))

        # generate the set of pixels to occupy
        num_of_pixels = randrange(0, width * height)
        fragment = set()

        # generate set of coordinates with constraints adherence. Format: ((x,y),(a,b,c,d)) where (a,b,c,d) is color and (x,y) are coordinates
        # TODO:
        # - implement address-based adherence
        # - implement line type adherence

        color_constraint = artwork.constraint.get_color()

        for i in range(num_of_pixels):
            coordinates = (randrange(x_coordinate, x_coordinate + width + 1), randrange(y_coordinate, y_coordinate + height + 1))

            pixel_info = (coordinates, color_constraint)
            fragment.add(pixel_info)

        return fragment

