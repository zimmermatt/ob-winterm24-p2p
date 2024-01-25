#!/usr/bin/env python3
"""
Module to manage ArtFragment

ArtFragment class allows us to instantiate a fragment for an Artwork instance
"""

import logging
from dataclasses import dataclass
from commission.artwork import Artwork
from commission.artwork import Pixel


@dataclass(frozen=True)
class ArtFragment:
    """
    Class to create ArtFragment
    - artwork (Artwork): Artwork that ArtFragment is contributing to
    - contributor (str): ID of peer generating the ArtFragment
    - pixels (set[Pixel]): set of pixels that fragment occupies
    """

    artwork: Artwork
    contributor: str
    pixels: frozenset[Pixel]

    logger = logging.getLogger("ArtFragment")
