"""
Module to manage a ledger for an Artwork.

The Ledger class allows us to maintain a history of ownership for an Artwork.
"""

import hashlib
import logging
import collections

logger = logging.getLogger("Ledger")


class Ledger:
    """Class to manage a Ledger for a single Artwork."""

    def __init__(self) -> None:
        self.queue = collections.deque()

    def add_owner(self, peer):
        """
        Add a new owner to the ledger.
        """

        previous_hash = self.queue[-1][1] if len(self.queue) > 0 else b""
        new_hash = hashlib.sha256(peer.keys["public"].encode()).digest()
        combined_hash = previous_hash + new_hash
        self.queue.append((peer, hashlib.sha256(combined_hash).digest()))

    def verify_integrity(self):
        """
        Verify the integrity of the ledger.
        """

        for i in range(1, len(self.queue)):
            previous_hash = self.queue[i - 1][1]
            current_hash = self.queue[i][1]
            expected_hash = hashlib.sha256(
                previous_hash
                + hashlib.sha256(self.queue[i][0].keys["public"].encode()).digest()
            ).digest()

            if current_hash != expected_hash:
                return False

        return True
