#!/usr/bin/env python3
"""
Module to manage trade response functionality.

OfferResponse class allows us to respond to a trade Announcement
"""

from commission.artwork import Artwork


class OfferResponse:
    """
    Class to manage exchange responses
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        exchange_id: str,
        artwork: Artwork,
        price: int,
        exchange_type: str,
        exchanger_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferResponse class.
        """

        self.exchange_id = exchange_id
        self.artwork = artwork
        self.price = price
        self.exchange_type: exchange_type
        self.public_key = exchanger_public_key

    def get_exchange_id(self):
        """
        Returns the id of the exchange.
        """

        return self.exchange_id

    def get_artwork(self):
        """
        Returns the artwork that is being exchanged.
        """

        return self.artwork

    def get_price(self):
        """
        Returns the price from the OfferAnnouncement.
        """

        return self.price

    def get_exchange_type(self):
        """
        Returns the exchange type from the OfferAnnouncement.
        """

        return self.exchange_type

    def get_exchanger_public_key(self):
        """
        Returns the public key of the originator of the exchange response.
        """

        return self.public_key
