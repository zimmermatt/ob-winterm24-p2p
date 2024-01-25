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

    def __init__(self, public_key):
        """Initialize the ledger by creating an empty list of transactions and
        setting the last_hash to None."""

        self.transactions = []
        self.last_hash = None
        self.public_key = public_key

    def add_transaction(self, public_key):
        """Add new ownder to the ledger."""
        peer_hash = self.hash_transaction(public_key)
        if self.last_hash:
            assert peer_hash == self.last_hash, "Invalid transaction"
        self.transactions.append(peer_hash)
        self.last_hash = self.hash_transaction(peer_hash)

    def get_transactions(self):
        """Return the history of owners."""
        return self.transactions

    def hash_transaction(self, public_key):
        """Hash the new owner's public key."""
        transaction_string = json.dumps(public_key.__dict__, sort_keys=True)
        return hashlib.sha1(transaction_string.encode()).digest()
