#!/usr/bin/env python3
"""
Module to manage coordinates class

Coordinate class allows us to create a coordinates with x,y values
"""


class Coordinates:
    """
    Class to manage coordinates
    """

    def __init__(self, x: int, y: int):
        """
        Initializes an instance of the Coordinates class.
        - x (int): x-coordinate
        - y (int): y-coordinate
        """
        self.x = self.check_coordinate(x)
        self.y = self.check_coordinate(y)

    def check_coordinate(self, coordinate):
        """
        If coordinate < 0, throws error
        """
        if coordinate < 0:
            raise ValueError("coordinate must be greater than or equal to 0.")
        return coordinate

    def create_bounds(self, width, height):
        """
        Create bounds in accordance to coordinates and width, height
        """
        return (1 + width - self.x, 1 + height - self.y)
