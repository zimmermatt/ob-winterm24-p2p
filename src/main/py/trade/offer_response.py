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
        artwork_ledger_key: str,
        originator_public_key: str = "",
    ):
        """
        Initializes an instance of the OfferResponse class.
        - trade_id (str): The trade id to respond to.
        """
        self.trade_id = trade_id
        self.artwork_ledger_key = artwork_ledger_key
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

    def get_artwork_ledger_key(self):
        """
        Returns the artwork ledger key to respond to.
        """

        return self.artwork_ledger_key
