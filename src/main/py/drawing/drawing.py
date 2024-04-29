#!/usr/bin/env python3
"""
Module to manage namedtuples related to drawing
"""

from collections import namedtuple

Coordinates = namedtuple("Coordinates", ["x", "y"])
Coordinates.__annotations__ = {"x": int, "y": int}

Color = namedtuple("Color", ["r", "g", "b", "a"], defaults=(255,) * 4)
Color.__annotations__ = {"r": int, "g": int, "b": int, "a": int}

Pixel = namedtuple("Pixel", ["coordinates", "color"])
Pixel.__annotations__ = {"coordinates": Coordinates, "color": Color}

Constraint = namedtuple("Constraint", ["palette_limit", "line_type"])
Constraint.__annotations__ = {"palette_limit": int, "line_type": str}
