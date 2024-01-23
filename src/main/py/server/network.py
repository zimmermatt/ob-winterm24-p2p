#!/usr/bin/env python3
""" This module contains the NewServer class. """

from kademlia.network import Server
from server.protocol import NewProtocol


class NewServer(Server):
    """
    A custom server class that extends the functionality of the base Server class.

    Args:
        ksize (int): The size of the k-buckets in the Kademlia DHT.
        alpha (int): The concurrency parameter for network operations.
        id (bytes): The ID of the server node.
        storage (Storage): The storage object used to store and retrieve data.
        store_callback (callable): A callback function called when data is stored.

    Attributes:
        store_callback (callable): A callback function called when data is stored.

    """

    def __init__(self, store_callback, ksize=20, alpha=3):
        """
        Initializes a new instance of the NewServer class.

        Args:
            ksize (int): The size of the k-buckets in the Kademlia DHT.
            alpha (int): The concurrency parameter for network operations.
            store_callback (callable): A callback function called when data is stored.

        """
        self.store_callback = store_callback
        # Call the parent class's __init__ with the new protocol
        super().__init__(ksize, alpha)

    def _create_protocol(self):
        """
        Creates a new instance of the NewProtocol class.

        Returns:
            NewProtocol: A new instance of the NewProtocol class.

        """
        return NewProtocol(self.node, self.storage, self.ksize, self.store_callback)
