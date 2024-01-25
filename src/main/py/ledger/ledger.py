"""
Module to manage a ledger for an Artwork.

The Ledger class allows us to add owners...
"""

from peer.peer import Peer

# original if the first in the ledger is the originator's blah blah blah...


class Ledger:
    """Class to manage a Ledger for a single Artwork."""

    def __init__(self) -> None:
        """Initialize the ledger by creating an empty list for the history
        of the ledger and creating the newest owner."""

        self.ledger_history = []
        self.curr_owner = None  # initialize it to the last owner or
        #                    none if that owner doesn't exist (Originator)

    def add_owner(self, peer: Peer):
        """Add a new owner to a ledger."""

        self.curr_owner = peer.keys["public"]
        self.ledger_history.append(self.curr_owner)

    def get_history(self):
        """Return the history of the ledger."""

        return self.ledger_history
