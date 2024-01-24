#!/usr/bin/env python3
""" This module contains the NewServer class. """

from kademlia.network import Server
from server.protocol import NotificationProtocol


class NotifyingServer(Server):
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

    def __init__(self, data_stored_callback, ksize=20, alpha=3, node_id=None):
        """
        Initializes a new instance of the NewServer class.

        Args:
            ksize (int): The size of the k-buckets in the Kademlia DHT.
            alpha (int): The concurrency parameter for network operations.
            store_callback (callable): A callback function called when data is stored.

        """
        self.data_stored_callback = data_stored_callback
        # Call the parent class's __init__ with the new protocol
        super().__init__(ksize, alpha, node_id=node_id)

    def _create_protocol(self):
        """
        Creates a new instance of the NewProtocol class.

        Returns:
            NewProtocol: A new instance of the NewProtocol class.

        """
        return NotificationProtocol(
            self.node, self.storage, self.ksize, self.data_stored_callback
        )
