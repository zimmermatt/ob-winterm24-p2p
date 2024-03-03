"""
Module to manage a ledger for an Artwork.

The Ledger class allows us to maintain a history of ownership for an Artwork.
"""

import hashlib
import logging

logger = logging.getLogger(__name__)


class Ledger:
    """Class to manage a Ledger for a single Artwork."""

    def __init__(self) -> None:
        self.stack = []
        self.top_of_stack = None

    def add_owner(self, peer):
        """
        Add a new owner to the ledger.
        """

        if not hasattr(peer, "keys"):
            logger.error("The owner must have a 'keys' attribute.")
            return

        if self.top_of_stack is not None:
            previous_hash = self.top_of_stack.digest()
        else:
            previous_hash = b""

        new_hash = hashlib.sha256(peer.keys["public"].encode()).digest()
        combined_hash = previous_hash + new_hash
        self.top_of_stack = hashlib.sha256(combined_hash)
        self.stack.append((peer.keys["public"], self.top_of_stack.digest()))

    def verify_integrity(self):
        """
        Verify the integrity of the ledger.
        """

        for i in range(1, len(self.stack)):
            previous_hash = self.stack[i - 1][1]
            current_hash = self.stack[i][1]
            expected_hash = hashlib.sha256(
                previous_hash + hashlib.sha256(self.stack[i][0].encode()).digest()
            ).digest()

            if current_hash != expected_hash:
                return False

        return True
