#!/usr/bin/env python3
"""
Module to manage artwork commission class

Artwork class allows us to create a commission, generate a file descriptor
"""

import random
from collections import namedtuple
from datetime import datetime, timedelta
from drawing.coordinates import Coordinates
from drawing.color import Color
from peer.ledger import Ledger
import utils

Pixel = namedtuple("Pixel", ["coordinates", "color"])
Pixel.__annotations__ = {"coordinates": Coordinates, "color": Color}
Constraint = namedtuple("Constraint", ["color", "line_type"])
Constraint.__annotations__ = {"color": Color, "line_type": str}


class Artwork:
    """
    Class to manage artwork commissions
    """

    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        width: float,
        height: float,
        wait_time: timedelta,
        ledger: Ledger,
        constraint: Constraint = None,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the Artwork class.
        - width (int): The width of the artwork in pixels.
        - height (float): The height of the artwork in pixels.
        - wait_time (timedelta): The wait time for the artwork as a timedelta.
        - constraint (Constraint): Constraint instance set to the artwork.
        - ledger: An instance of the Ledger class.
        """
        self.width = width
        self.height = height
        self.wait_time = wait_time
        self.commission_complete = False
        if constraint is None:
            self.constraint = self.generate_random_constraint()
        else:
            self.constraint = constraint
        self.key = utils.generate_random_sha1_hash()
        start_time = datetime.now()
        self.end_time = start_time + self.wait_time
        self.originator_public_key = originator_public_key
        self.ledger = ledger

    def generate_random_constraint(self):
        """
        Generates a random constraint.
        """
        random_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        random_line_type = "solid"
        return Constraint(random_color, random_line_type)

    def get_remaining_time(self):
        """
        Returns the remaining wait time until the artwork is complete in seconds.
        """
        remaining_time = self.end_time - datetime.now()
        return max(0, remaining_time.total_seconds())

    def get_key(self):
        """
        Returns the file descriptor for the artwork.
        """
        return self.key

    def set_complete(self):
        """
        Sets the commission status to complete.
        """
        self.commission_complete = True
        return self
