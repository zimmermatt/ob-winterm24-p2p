#!/usr/bin/env python3
"""
Module to manage trade response functionality.

OfferResponse class allows us to respond to a trade Announcement
"""


class OfferResponse:
    """
    Class to manage trade responses
    """

    def __init__(
        self,
        trade_id: str,
        artwork_id: str,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferResponse class.
        - trade_id (str): The trade id to respond to.
        """
        self.trade_id = trade_id
        self.offer_id = artwork_id
        self.originator_public_key = originator_public_key

    def get_trade_id(self):
        """
        Returns the trade id to respond to.
        """
        return self.trade_id

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the trade response.
        """
        return self.originator_public_key

    def get_offer_ledger_id(self):
        """
        Returns the offer ledger id to respond to.
        """
        return self.offer_id
