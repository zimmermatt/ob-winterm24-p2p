"""
Module to manage a ledger for an Artwork.

The Ledger class allows us to add owners...
"""

import hashlib
import json
from peer.peer import Peer


class Ledger:
    """Class to manage ledgers for Art Collectors."""

    def __init__(self):
        """Initialize the ledger by creating an empty list for the history
        of the ledger and creating the newest owner."""

        self.ledger_history = []
        self.owner_key = None

    def add_owner(self, peer: Peer):
        """Add a new owner to a ledger."""

        self.owner_key = self.public_key(peer)
        self.ledger_history.append(self.owner_key)

    def get_history(self):
        """Return the history of the ledger."""
        return self.ledger_history

    def public_key(self, peer: Peer):
        """Hash the transaction."""
        peer_string = json.dumps(peer.__dict__, sort_keys=True)
        return hashlib.sha1(peer_string.encode()).digest()
