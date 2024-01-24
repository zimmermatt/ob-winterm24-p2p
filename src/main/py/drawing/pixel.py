#!/usr/bin/env python3
"""
Module to manage pixel class

Pixel class allows us to create a pixel with coordinates and color  values
"""

from drawing.color import Color
from drawing.coordinates import Coordinates


class Pixel:
    """
    Class to manage color
    """

    def __init__(self, coordinates: Coordinates, color: Color):
        """
        Initializes an instance of the Pixel class.
        - coordinates (Coordinates): represents Pixel's location.
        - color (Color): represents Pixel's color.
        """
        self.coordinates = coordinates
        self.color = color

    def get_coordinates(self):
        """
        Get coordianates of pixel.
        """
        return self.coordinates

    def get_color(self):
        """
        Get color of pixel.
        """
        return self.color
