#!/usr/bin/env python3
"""
Module to manage ArtFragmentGenerator

ArtFragmentGenerator class allows us to create an instance of ArtFragment
"""

import logging
import random
from random import randrange
from collections import namedtuple
from commission.artwork import Artwork, Pixel
from commission.artfragment import ArtFragment
from drawing.coordinates import Coordinates

Subcanvas = namedtuple("SubCanvas", ["coordinates", "dimensions"])
Subcanvas.__annotations__ = {"coordinates": Coordinates, "dimensions": tuple[int, int]}

logger = logging.getLogger("ArtFragmentGenerator")


def generate_fragment(artwork: Artwork, contributor: str):
    """
    Generates an ArtFragment instance
    - artwork (Artwork): Artwork that the ArtFragment is intended for.
    - contributor (str): Peer ID that created the ArtFragment.
    """
    subcanvas = generate_subcanvas(artwork.width, artwork.height)

    pixels = generate_pixels(subcanvas)
    fragment = ArtFragment(artwork.get_key(), contributor, pixels)
    return fragment


def generate_subcanvas(width: int, height: int):
    """
    Generates starting (x,y) coordinates with width and height adhering to artwork
    """
    x_coordinate = randrange(0, width)
    y_coordinate = randrange(0, height)
    coordinates = Coordinates(x_coordinate, y_coordinate)
    bounds = coordinates.create_bounds(width, height)

    subcanvas_width = randrange(1, bounds[0])
    subcanvas_height = randrange(1, bounds[1])

    subcanvas = Subcanvas(
        coordinates=coordinates, dimensions=(subcanvas_width, subcanvas_height)
    )
    return subcanvas


def generate_pixels(subcanvas: tuple[tuple[int, int], tuple[int, int]]):
    """
    Generate a list of pixel info that adheres to coordiantes, dimensions, constraints

    TODO:
    - implement address-based adherence
    - implement line type adherence
    """
    coordinates = subcanvas.coordinates
    dimensions = subcanvas.dimensions
    color_constraint = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

    x_coordinate = coordinates.x
    y_coordinate = coordinates.y

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
