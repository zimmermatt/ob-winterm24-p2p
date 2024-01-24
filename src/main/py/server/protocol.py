"""
Module for Kademlia library rpc_store() callback
"""
import asyncio
from kademlia.protocol import KademliaProtocol


class NotificationProtocol(KademliaProtocol):
    """
    Class for Kademlia library rpc_store() callback
    """

    def __init__(self, source_node, storage, ksize, data_stored_callback) -> None:
        """
        Initialize a new instance of NewProtocol.

        Args:
            source_node (Node): The source node.
            storage (Storage): The storage object.
            ksize (int): The k parameter for Kademlia.
            callback_function (function): The callback function to be called on rpc_store
        """
        self.data_stored_callback = data_stored_callback
        super().__init__(source_node, storage, ksize)

    def rpc_store(self, sender, nodeid, key, value):
        """
        Override the rpc_store method from the parent class.

        Args:
            sender (Node): The sender node.
            nodeid (bytes): The node ID.
            key (bytes): The key to store.
            value (bytes): The value to store.
        """
        super().rpc_store(sender, nodeid, key, value)
        asyncio.create_task(self.data_stored_callback(key, value))
