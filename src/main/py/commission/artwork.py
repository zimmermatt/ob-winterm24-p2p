#!/usr/bin/env python3
"""
Module to manage artwork commission class

Artwork class allows us to create a commission, generate a file descriptor
"""

from datetime import datetime, timedelta
import utils


class Artwork:
    """
    Class to manage artwork commissions
    """

    def __init__(
        self,
        width: float,
        height: float,
        wait_time: timedelta,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the Artwork class.
        - width (float): The width of the artwork in pixels.
        - height (float): The height of the artwork in pixels.
        - wait_time (timedelta): The wait time for the artwork as a timedelta.
        """
        self.width = width
        self.height = height
        self.wait_time = wait_time
        self.commission_complete = False
        self.key = utils.generate_random_sha1_hash()
        start_time = datetime.now()
        self.end_time = start_time + self.wait_time
        self.originator_public_key = originator_public_key

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
