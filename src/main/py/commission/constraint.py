#!/usr/bin/env python3
"""
Module to manage constraint class

Constraint class allows us to add constraints to an artwork
"""

from drawing.color import Color


class Constraint:
    """
    Class to manage constraint
    """

    def __init__(self, color: Color, line_type: str):
        """
        Initializes an instance of the Constraint class.
        - color (Color): color constraint.
        - line_type (str): line constraint.
        """
        self.color = color
        self.line_type = line_type

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
