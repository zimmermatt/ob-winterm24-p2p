"""
Module to manage a ledger for an Artwork.

The Ledger class allows us to maintain a history of ownership for an Artwork.
"""

import hashlib


class Ledger:
    """Class to manage a Ledger for a single Artwork."""

    def __init__(self) -> None:
        self.stack = []
        self.top_of_stack = None

    def add_owner(self, peer):
        """
        Add a new owner to the ledger.
        """

        try:
            if not hasattr(peer, "keys"):
                raise ValueError("The owner must have a 'keys' attribute.")

            if self.top_of_stack is not None:
                previous_hash = self.top_of_stack.digest()
            else:
                previous_hash = b""

            new_hash = hashlib.sha256(peer.keys["public"].encode()).digest()
            combined_hash = previous_hash + new_hash
            self.top_of_stack = hashlib.sha256(combined_hash)
            self.stack.append((peer, self.top_of_stack.digest()))
        except (ValueError, TypeError, AttributeError) as e:
            print(f"An error occurred while adding owner: {e}")

    def get_current_owner(self):
        """
        Get the current owner of the artwork.
        """

        try:
            if not self.stack:
                raise ValueError("The ledger is empty.")

            return self.stack[-1][0]
        except (ValueError, TypeError, AttributeError) as e:
            print(f"An error occurred while getting current owner: {e}")
            return None

    def get_current_version(self):
        """
        Get the current version of the ledger.
        """

        try:
            if not self.stack:
                raise ValueError("The ledger is empty.")

            return self.stack[-1][1]
        except (ValueError, TypeError, AttributeError) as e:
            print(f"An error occurred while getting current version: {e}")
            return b""

    def get_specified_version(self, index: int):
        """
        Get the specified version of the ledger.
        """

        try:
            return self.stack[index][1]
        except IndexError:
            print(f"No version found at index {index}")
            return b""

    def get_specified_owner(self, index: int):
        """
        Get the specified owner of the artwork.
        """

        try:
            return self.stack[index][0]
        except IndexError:
            print(f"No owner found at index {index}")
            return None

    def get_history(self):
        """
        Get the history of the ledger.
        """

        return self.stack

    def verify_integrity(self):
        """
        Verify the integrity of the ledger.
        """

        if not self.stack:
            raise ValueError("The ledger is empty.")

        for i in range(1, len(self.stack)):
            previous_hash = self.stack[i - 1][1]
            current_hash = self.stack[i][1]
            expected_hash = hashlib.sha256(
                previous_hash
                + hashlib.sha256(self.stack[i][0].keys["public"].encode()).digest()
            ).digest()

            if current_hash != expected_hash:
                return False

        return True
