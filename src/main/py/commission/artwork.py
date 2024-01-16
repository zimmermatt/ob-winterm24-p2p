#!/usr/bin/env python3
"""
Module to manage artwork commission class

Artwork class allows us to create a commission, generate a file descriptor
"""


class Artwork:
    """
    Class to manage artwork commissions
    """

    def __init__(self, width, height, wait_time):
        """
        Initializes an instance of the Artwork class.
        Args:
            width (int): The width of the artwork.
            height (int): The height of the artwork.
            wait_time (float): The wait time for the artwork.
        Returns:
            Artwork: The initialized Artwork object.
        """
        self.width = width
        self.height = height
        self.wait_time = wait_time
        self.commission_complete = False
        self.ipfs_file_descriptor = self.generate_file_descriptor()

    def generate_file_descriptor(self):
        """
        Generates a file descriptor for the artwork.

        Returns:
            str: The generated file descriptor.
        """
        return "placeholder_ipfs_file_descriptor"

    def get_wait_time(self):
        """
        Returns the wait time for the artwork.

        Returns:
            float: The wait time for the artwork.
        """
        return self.wait_time
    
    def get_file_descriptor(self):
        """
        Returns the file descriptor for the artwork.

        Returns:
            str: The file descriptor for the artwork.
        """
        return self.ipfs_file_descriptor

    def set_complete(self):
        """
        Sets the commission status to complete.

        Returns:
            Artwork: The updated Artwork object.
        """
        self.commission_complete = True
        return self
