#!/usr/bin/env python3
"""
Module to manage artwork commission class

Artwork class allows us to create a commission, generate a file descriptor
"""

import string
import random
import hashlib
from datetime import datetime, timedelta
from enum import Enum
from commission.constraint import Constraint


class TradeStatus(Enum):
    """
    Enum to manage trade status
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    RECEIVED = "received"
    COMPLETED = "completed"


class Artwork:
    """
    Class to manage artwork commissions
    """

    def __init__(
        self,
        width: float,
        height: float,
        wait_time: timedelta,
        constraint: Constraint = None,
    ):
        """
        Initializes an instance of the Artwork class.
        - width (float): The width of the artwork in pixels.
        - height (float): The height of the artwork in pixels.
        - wait_time (timedelta): The wait time for the artwork as a timedelta.
        - constraints (list[Constraint]): Constraints set to the artwork.
        """

        self.width = width
        self.height = height
        self.wait_time = wait_time
        self.commission_complete = False
        self.constraint = constraint
        self.key = self.generate_key()
        start_time = datetime.now()
        self.end_time = start_time + self.wait_time
        self.trade_status = {}

    def generate_key(self):
        """
        Generates a random SHA-1 hash as a file descriptor for the artwork.
        """

        key_length = 10
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(key_length))
        sha1_hash = hashlib.sha1(random_string.encode()).digest()
        return sha1_hash

    def get_remaining_time(self):
        """
        Returns the remaining wait time until the artwork is complete in seconds.
        """

        remaining_time = self.end_time - datetime.now()
        return max(0, remaining_time.total_seconds())

    def get_key(self):
        """
        Returns the file descriptor for the artwork.
        """

        return self.key

    def get_constraint(self):
        """
        Returns the constraint for the artwork.
        """

        return self.constraint

    def set_constraint(self, constraint: Constraint):
        """
        Set a constraint to the artwork.
        """

        self.constraint = constraint
        return self

    def set_complete(self):
        """
        Sets the commission status to complete.
        """

        self.commission_complete = True
        return self

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

        return self.trade_status[peer]

    def is_all_trade_complete(self):
        """
        Returns True if all trades, whether it be an acceptance or rejection, are complete,
        False otherwise.
        """

        return all(
            self.get_trade_status(peer) == TradeStatus.COMPLETED.value
            for peer in self.trade_status
        )
