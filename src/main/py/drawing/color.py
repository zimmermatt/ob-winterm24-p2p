#!/usr/bin/env python3
"""
Module to manage color class

Color class allows us to create a color with RGBA values
"""


class Color:
    """
    Class to manage color
    """

    def __init__(self, r: int, g: int, b: int, a: int):
        """
        Initializes an instance of the Color class.
        - r (int): red channel value
        - g (int): green channel value
        - b (int): blue channel value
        - a (int): alpha (opacity) channel value
        """
        self.channels = self.check_color([r, g, b, a])

    def check_color(self, channels):
        """
        Create a valid color tuple based on input
        """
        checked_color = []
        for channel in channels:
            checked_channel = self.check_channel(channel)
            checked_color.append(checked_channel)
        return tuple(checked_color)

    def check_channel(self, channel):
        """
        If a channel < 0, or > 255, raise error.
        """
        if channel < 0:
            raise ValueError("channel value must be non-negative.")
        if channel > 255:
            raise ValueError("channel value must be less than 256.")
        return channel
