"""
Module to manage artwork ledger functionality.

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
        self.top = None

    def add_owner(self, peer_public_key: str):
        """
        Add a new owner to the ledger.
        """

        previous_hash = self.top if self.top else b""
        new_hash = hashlib.sha256(peer_public_key.encode()).digest()
        combined_hash = previous_hash + new_hash
        self.top = hashlib.sha256(combined_hash).digest()
        self.queue.append((peer_public_key, self.top))

    def get_owner(self):
        """
        Get the current owner of the artwork.
        """

        return self.queue[-1][0]

    def get_previous_owner(self):
        """
        Get the previous owner of the artwork.
        """

        return self.queue[-2][0] if len(self.queue) > 1 else None

    def get_originator(self):
        """
        Get the first owner of the artwork.
        """

        return self.queue[0][0]

    def get_owner_history(self):
        """
        Get the owner history of the artwork with hashes.
        """

        return self.queue

    def verify_integrity(self):
        """
        Verify the integrity of the ledger.
        """

        for i in range(1, len(self.queue)):
            previous_hash = self.queue[i - 1][1]
            current_hash = self.queue[i][1]
            expected_hash = hashlib.sha256(
                previous_hash + hashlib.sha256(self.queue[i][0].encode()).digest()
            ).digest()

            if current_hash != expected_hash:
                return False

        return True
