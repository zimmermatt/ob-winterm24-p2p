#!/usr/bin/env python3
"""
Module to manage ArtFragment

ArtFragment class allows us to instantiate a fragment for an Artwork instance
"""

import logging
from dataclasses import dataclass
from commission.artwork import Artwork
from drawing.pixel import Pixel


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
    pixels: set[Pixel]

    logger = logging.getLogger("ArtFragment")

    def get_pixels(self):
        """
        Get the pixels occupied by the fragment
        """
        return self.pixels

    def get_contributor(self):
        """
        Get the contributor who made the fragment
        """
        return self.contributor

    def get_artwork(self):
        """
        Get the artwork that the fragment targets
        """
        return self.artwork
