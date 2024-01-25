"""
Module to manage a blockchain-based ledger.

Ledger class allows us to add transactions to the ledger and retrieve the
transactions.
"""

import hashlib
import json


class Ledger:
    """Class to manage ledgers for Art Collectors."""

    def __init__(self):
        """Initialize the ledger by creating an empty list of transactions and
        setting the last_hash to None."""

        self.transactions = []
        self.last_hash = None

    def add_transaction(self, transaction):
        """Add a transaction to the ledger."""
        transaction_hash = self.hash_transaction(transaction)
        if self.last_hash:
            assert transaction_hash == self.last_hash, "Invalid transaction"
        self.transactions.append(transaction)
        self.last_hash = self.hash_transaction(transaction)

    def get_transactions(self):
        """Return the list of transactions."""
        return self.transactions

    def hash_transaction(self, transaction):
        """Hash the transaction."""
        transaction_string = json.dumps(transaction.__dict__, sort_keys=True)
        return hashlib.sha1(transaction_string.encode()).digest()

    # def check_original_artwork(self, transaction):
    #     """Check if the artwork is an original."""
    #     check pull request to see if
