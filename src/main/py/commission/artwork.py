#!/usr/bin/env python3
"""
Module to manage artwork commission class

Artwork class allows us to create a commission, generate a file descriptor
"""

import string
import random
from datetime import datetime, timedelta


class Artwork:
    """
    Class to manage artwork commissions
    """

    def __init__(self, width, height, wait_time):
        """
        Initializes an instance of the Artwork class.
        - width (float): The width of the artwork in pixels.
        - height (float): The height of the artwork in pixels.
        - wait_time (int): The wait time for the artwork in minutes.
        """
        self.width = width
        self.height = height
        self.wait_time = timedelta(seconds=wait_time)
        self.commission_complete = False
        self.key = self.generate_key()
        self.start_time = datetime.now()

    def generate_key(self):
        """
        Generates a file descriptor for the artwork.
        """
        key_length = 10
        characters = string.ascii_letters + string.digits
        key = "".join(random.choice(characters) for _ in range(key_length))
        return key

    def get_wait_time(self):
        """
        Returns the remaining wait time until the artwork is complete in seconds.
        """
        remaining_time = (self.start_time + self.wait_time) - datetime.now()
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
