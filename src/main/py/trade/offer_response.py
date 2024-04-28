#!/usr/bin/env python3
"""
Module to manage trade response functionality.

OfferResponse class allows us to respond to a trade Announcement
"""


class OfferResponse:
    """
    Class to manage exchange responses
    """

    def __init__(
        self,
        exchange_id: str,
        artwork_id: str,
        price: int,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferResponse class.
        """

        self.exchange_id = exchange_id
        self.artwork_id = artwork_id
        self.price = price
        self.originator_public_key = originator_public_key

    def get_exchange_id(self):
        """
        Returns the exchange id to respond to.
        """

        return self.exchange_id

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the exchange response.
        """

        return self.originator_public_key

    def get_artwork_id(self):
        """
        Returns the artwork ledger key to respond to.
        """

        return self.artwork_id

    def get_price(self):
        """
        Returns the price from the OfferAnnouncement.
        """

        return self.price
