"""
Module to manage a blockchain-based ledger.

Ledger class allows us to add transactions to the ledger and retrieve the
transactions.
"""

import hashlib
import json
from peer.peer import Peer


class Ledger:
    """Class to manage ledgers for Art Collectors."""

    def __init__(self):
        """Initialize the ledger by creating an empty list of transactions and
        creating the newest owner."""

        self.transactions = []
        self.owner_key = None

    def add_owner(self, peer: Peer):
        """Add a new owner to a ledger."""

        self.transactions.append(peer)
        self.owner_key = self.public_key(peer)

    def get_transactions(self):
        """Return the list of transactions."""
        return self.transactions

    def public_key(self, peer: Peer):
        """Hash the transaction."""
        peer_string = json.dumps(peer.__dict__, sort_keys=True)
        return hashlib.sha1(peer_string.encode()).digest()
