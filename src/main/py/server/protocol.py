"""
Module for Kademlia library rpc_store() callback

ADD HERE
"""
from kademlia.protocol import KademliaProtocol


class NewProtocol(KademliaProtocol):
    """
    Class for Kademlia library rpc_store() callback
    """

    def __init__(self, source_node, storage, ksize, callback_function) -> None:
        self.callback_function = callback_function
        super().__init__(source_node, storage, ksize)

    def rpc_store(self, sender, nodeid, key, value):
        super().rpc_store(sender, nodeid, key, value)

        # get value (Python object, send as parameter in generate_fragment)
        self.peer_instance.generate_fragment()

        # send fragment back to originator
        self.peer_instance.recieve_fragment()
        # add parameters
