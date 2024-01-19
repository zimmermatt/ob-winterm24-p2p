#!/usr/bin/env python3
"""
Module to manage constraint class

Constraint class allows us to add constraints to an artwork
"""

import string


class Constraint:
    """
    Class to manage constraint
    """

    def __init__(self, color: tuple[int, int, int, int], line_type: string):
        """
        Initializes an instance of the Constraint class.
        - color (tuple(int, int, int, int)): color constraint.
        - line_type (float): line constraint.
        """
        self.color = self.normalize_color(color)
        self.line_type = line_type

    def normalize_color(self, color):
        """
        If a channel in color tuple < 0, make it 0. If it is > 255, make it 255.
        """
        return_color = []
        for channel in color:
            if channel < 0:
                channel = 0
            elif channel > 255:
                channel = 255
            return_color.append(channel)

        return tuple(return_color)

    def get_color(self):
        """
        Returns constraint's color
        """
        return self.color

    def get_line_type(self):
        """
        Returns constraint's line type
        """
        return self.line_type
