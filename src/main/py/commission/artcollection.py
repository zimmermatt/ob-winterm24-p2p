"""
Module to manage art collections for Art Collectors.
"""

from enum import Enum

# TODO: Deal with ledgers
#      Handle what happens when a trade is accepted or rejected


class TradeStatus(Enum):
    """
    Enum to manage trade status
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    RECEIVED = "received"
    COMPLETED = "completed"


class ArtCollection:
    """
    Class to manage art collections for Art Collectors.
    """

    def __init__(self) -> None:
        self.trade_status = {}
        self.artworks = []

    def get_artworks(self):
        """
        Returns the artworks in the collection.
        """

        return self.artworks

    def add_artwork(self, artwork):
        """
        Add an artwork to the collection.
        """

        self.artworks.append(artwork)

    def remove_artwork(self, artwork):
        """
        Remove an artwork from the collection.
        """

        self.artworks.remove(artwork)

    def set_trade_status(self, peer, status: TradeStatus):
        """
        Sets the trade status for the given peer.
        """

        self.trade_status[peer] = status.value
        return self

    def get_trade_status(self, peer):
        """
        Returns the trade status for the given peer.
        """

        # handle when a peer isn't in the trade_status dictionary

        return self.trade_status[peer]

    # def trade_accepted(self, peer):
    # remove from pending list
    # add ownership to ledger (blockchain)
    # swap artworks
    # reply_trade_status_recieved

    # def trade_rejected(self, peer):

    def is_all_trade_complete(self):
        """
        Returns True if all trades, whether it be an acceptance or rejection, are complete,
        False otherwise.
        """

        return all(
            self.get_trade_status(peer) == TradeStatus.COMPLETED.value
            for peer in self.trade_status
        )
