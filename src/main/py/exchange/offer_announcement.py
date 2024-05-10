#!/usr/bin/env python3
"""
Module to manage exchange announcement functionality.

OfferAnnouncement class allows us to create a exchange announcement
"""

from commission.artwork import Artwork


class OfferAnnouncement:
    """
    Class to manage exchange announcements
    """

    def __init__(
        self,
        artwork: Artwork,
        price: int,
        exchange_type: str,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferAnnouncement class.
        """

        self.artwork = artwork
        self.price = price
        self.exchange_type = exchange_type
        self.originator_public_key = originator_public_key
        self.deadline_reached = False

    def get_artwork(self):
        """
        Returns the artwork that is exchanged
        """

        return self.artwork

    def get_price(self):
        """
        Returns the purchase price for the artwork.
        """

        return self.price

    def get_exchange_type(self):
        """
        Returns the exchange type for the announcmnet (sale or trade).
        """

        return self.exchange_type

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the exchange announcement.
        """

        return self.originator_public_key
