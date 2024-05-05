#!/usr/bin/env python3
"""
Module to manage exchange announcement functionality.

OfferAnnouncement class allows us to create a exchange announcement
"""


class OfferAnnouncement:
    """
    Class to manage exchange announcements
    """

    def __init__(
        self,
        artwork_id: str,
        price: int,
        exchange_type: str,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferAnnouncement class.
        """

        self.artwork_id = artwork_id
        self.originator_public_key = originator_public_key
        self.price = price
        self.exchange_type = exchange_type
        self.deadline_reached = False

    def get_artwork_id(self):
        """
        Returns the artwork to be traded.
        """

        return self.artwork_id

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the exchange announcement.
        """

        return self.originator_public_key

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
