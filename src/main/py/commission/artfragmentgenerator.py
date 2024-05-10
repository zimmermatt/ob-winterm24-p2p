#!/usr/bin/env python3
"""
Module to manage ArtFragmentGenerator

ArtFragmentGenerator class allows us to create an instance of ArtFragment
"""

import logging
import random
from random import randrange
from collections import namedtuple
from commission.artwork import Artwork
from commission.artfragment import ArtFragment
from drawing.drawing import Coordinates, Pixel, Constraint, Color

Subcanvas = namedtuple("SubCanvas", ["coordinates", "dimensions"])
Subcanvas.__annotations__ = {"coordinates": Coordinates, "dimensions": tuple[int, int]}

logger = logging.getLogger("ArtFragmentGenerator")


def generate_fragment(
    artwork: Artwork,
    originator_id: int,
    contributor_signing_key: str,
    contributor_id: int,
) -> ArtFragment:
    """Generates an ArtFragment instance

    Args:
        artwork: Artwork that the ArtFragment is intended for.
        originator_id: ID of the peer that commissioned the artwork.
        contributor_signing_key: signing key of the peer that is contributing to the artwork.
        contributor_id: ID of the peer that is contributing to the artwork.

    Returns:
        ArtFragment: art fragment that adheres to artwork's constraint.
    """
    constraint = artwork.constraint
    subcanvas = generate_subcanvas(artwork.width, artwork.height)

    pixels = generate_pixels(originator_id, contributor_id, subcanvas, constraint)
    fragment = ArtFragment(artwork.get_key(), contributor_signing_key, pixels)
    return fragment


def get_bounds(coordinates: Coordinates, width: int, height: int) -> tuple[int, int]:
    """Get bounds of how big a subcanvas can be.

    Args:
        coordinates: starting coordinates of subcanvas.
        width: width of artwork.
        height: height of artwork.
    """
    bounds = (width - coordinates.x, height - coordinates.y)
    return bounds


def generate_subcanvas(width: int, height: int) -> Subcanvas:
    """Generates starting (x,y) coordinates with width and height within bounds of the artwork.

    Args:
        width: artwork's width.
        height: artwork's height.

    Returns:
        Subcanvas: a subcanvas that is within the artwork's width and height.
    """
    x_coordinate = randrange(0, width)
    y_coordinate = randrange(0, height)
    coordinates = Coordinates(x_coordinate, y_coordinate)

    bounds = get_bounds(coordinates, width, height)
    subcanvas_width = randrange(1, bounds[0] + 1)
    subcanvas_height = randrange(1, bounds[1] + 1)

    subcanvas = Subcanvas(
        coordinates=coordinates, dimensions=(subcanvas_width, subcanvas_height)
    )
    return subcanvas


def generate_pixels(
    originator_id: int,
    contributor_id: int,
    subcanvas: Subcanvas,
    constraint: Constraint = None,
) -> set:
    """Generate a list of pixel info that adheres to subcanvas and artwork's constraints.

    TODO:
    - implement line type adherence

    Args:
        originator_id : ID of the peer that commissioned the artwork.
        contributor_id: ID of the peer that is contributing to the artwork.
        subcanvas: the subcanvas that the contributor will draw on.
        constraint: Constraint of subcanvas. Defaults to None.

    Returns:
        set: a set of pixels with coordinates and colors adhering to subcanvas and constraints.
    """
    if constraint is not None:
        palette = get_palette(originator_id, contributor_id, constraint.palette_limit)
    else:
        palette = [
            Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        ]

    x_coordinate = subcanvas.coordinates.x
    y_coordinate = subcanvas.coordinates.y

    width = subcanvas.dimensions[0]
    height = subcanvas.dimensions[1]

    num_pixels = randrange(0, width * height)
    x_bound = x_coordinate + width
    y_bound = y_coordinate + height
    set_pixels = set()

    while num_pixels > 0:
        coordinates = Coordinates(
            randrange(x_coordinate, x_bound), randrange(y_coordinate, y_bound)
        )
        pixel = Pixel(coordinates, random.choice(palette))
        set_pixels.add(pixel)
        num_pixels -= 1

    return set_pixels


def get_palette(originator_id: int, contributor_id: int, palette_limit: int) -> list:
    """
    Get palette corresponding to palette_limit and distance from originator to contributor

    Args:
        originator_id: ID of the peer that commissioned the artwork.
        contributor_id: ID of the peer that is contributing to the artwork.
        palette_limit: the number of colors in palette

    Returns:
        list: a list of colors in the palette
    """

    distance = originator_id ^ contributor_id
    random.seed(distance)

    # Create an array of palette_limit*3 color channels
    channels = random.sample(range(0, 256), palette_limit * 3)

    # create a palette array of colors, each color being a 3-element tuple
    start = 0
    end = 3
    n = len(channels)
    palette = []

    while end <= n:
        color = Color(*channels[start:end])
        start = end
        end += 3
        palette.append(color)

    return palette
