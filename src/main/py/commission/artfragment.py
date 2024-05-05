#!/usr/bin/env python3
"""
Module to manage ArtFragment

ArtFragment class allows us to instantiate a fragment for an Artwork instance
"""

import logging
from dataclasses import dataclass
from drawing.drawing import Pixel


@dataclass(frozen=True)
class ArtFragment:
    """
    Class to create ArtFragment
    - artwork_id: ID of Artwork that fragment is contributing to.
    - contributor_signing_key: signing key of the peer that is contributing to the artwork.
    - pixels: set of pixels that fragment occupies.
    """

    artwork_id: str
    contributor_id: str
    pixels: frozenset[Pixel]

    logger = logging.getLogger("ArtFragment")
