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
        self.channels = self.normalize_color([r, g, b, a])

    def normalize_color(self, channels):
        """
        Create a valid color tuple based on input
        """
        normalized_color = []
        for channel in channels:
            normalized_channel = self.normalize_chanel(channel)
            normalized_color.append(normalized_channel)
        return tuple(normalized_color)

    def normalize_chanel(self, channel):
        """
        If a channel < 0, make it 0. If it is > 255, make it 255.
        """
        if channel < 0:
            channel = 0
        elif channel > 255:
            channel = 255
        return channel

    def get_channels(self):
        """
        Get channels of color.
        """
        return self.channels
