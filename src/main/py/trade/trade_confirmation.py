#!/usr/bin/env python3
"""
Module to manage trade confirmations.

TradeConfirmation class allows us to respond to a trade responses
"""


class TradeConfirmation:
    """
    Class to manage trade confirmations
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        trade_id: str,
        announced_offer_id: bytes,
        responded_offer_id: bytes,
        originator_public_key: str = "",
        accepted: bool = False,
    ):
        """
        Initializes an instance of the TradeConfirmation class.
        - trade_id (str): The trade id to confirm.
        """
        self.trade_id = trade_id
        self.announced_offer_id = announced_offer_id
        self.responded_offer_id = responded_offer_id
        self.originator_public_key = originator_public_key
        self.accepted = accepted

    def get_trade_id(self):
        """
        Returns the trade id to confirm.
        """
        return self.trade_id

    def get_originator_public_key(self):
        """
        Returns the public key of the originator of the trade confirmation.
        """
        return self.originator_public_key

    def get_announced_offer_id(self):
        """
        Returns the announced offer id to confirm.
        """
        return self.announced_offer_id
