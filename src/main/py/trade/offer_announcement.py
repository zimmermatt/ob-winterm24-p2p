#!/usr/bin/env python3
"""
Module to manage trade announcement functionality.

OfferAnnouncement class allows us to create a trade announcement
"""


class OfferAnnouncement:
    """
    Class to manage trade announcements
    """

    def __init__(
        self,
        artwork_id: str,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferAnnouncement class.
        - artwork (Artwork): The artwork to be traded.
        """
        self.artwork_id = artwork_id
        self.originator_public_key = originator_public_key
        self.deadline_reached = False

    def get_artwork_id(self):
        """
        Returns the artwork to be traded.
        """
        return self.artwork_id

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the trade announcement.
        """
        return self.originator_public_key
