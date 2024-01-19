#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""
import asyncio
from datetime import timedelta
import ipaddress
import pickle
import logging
import sys
import threading
import server as kademlia
from commission.artwork import Artwork


class Peer:
    """Class to manage peer functionality"""

    logger = logging.getLogger("Peer")

    def __init__(self, port: int, peer_network_address: str, kdm) -> None:
        """
        Initialize the Peer class by joining the kademlia network.

        Params:
        - peer_network_address (str): String containing the IP address and port number of a peer
          on the network separated by a colon.
        - port (int): The port number for the peer to listen on.
        """
        if peer_network_address is not None:
            try:
                network_ip_address, network_port_num = peer_network_address.split(":")
                self.network_ip_address = ipaddress.ip_address(network_ip_address)
                self.network_port_num = int(network_port_num)
            except ValueError as exc:
                raise ValueError(
                    "Invalid network address. Please provide a valid network address."
                ) from exc
        self.port = port
        self.kdm = kdm
        self.commissions = []
        self.deadline_timers = {}
        self.node = None

    def send_deadline_reached(self, commission: Artwork) -> None:
        """
        Mark the commission as complete, publish it on kademlia, and remove it from the list.
        """
        commission.set_complete()
        self.node.set(commission.get_key(), pickle.dumps(commission))

    def setup_deadline_timer(self, commission: Artwork) -> None:
        """
        Schedule the deadline notice for the commission.
        """
        deadline_seconds = commission.get_remaining_time()
        deadline_timer = threading.Timer(
            deadline_seconds, self.send_deadline_reached, args=(commission,)
        )
        self.deadline_timers[commission.get_key()] = deadline_timer
        deadline_timer.start()

    def send_commission_request(self, commission: Artwork) -> None:
        """
        Publish the commission on kademlia, add it to the list, and schedule the deadline notice.
        """
        self.node.set(commission.get_key(), pickle.dumps(commission))
        self.commissions.append(commission)
        self.setup_deadline_timer(commission)

    def commission_art_piece(self) -> None:
        """
        Get commission details from user input, create a commission, and send the request.
        """
        while True:
            try:
                width = float(input("Enter commission width: "))
                height = float(input("Enter commission height: "))
                wait_time = float(input("Enter wait time in seconds: "))
                commission = Artwork(width, height, timedelta(seconds=wait_time))
                self.send_commission_request(commission)
                break
            except ValueError:
                self.logger.error("Invalid input. Please enter a valid float.")

    def generate_piece(self, commission: Artwork):
        """Generate a piece of the artwork"""
        self.logger.info("Generating fragment")
        return commission

    def callback_function(self, key, value):
        """
        Callback function for when data is stored.

        Args:
            key (bytes): The key to store.
            value (bytes): The value to store.
        """
        self.logger.info("Data stored with key: %s", key)
        self.logger.info("Data stored with value: %s", value)
        artwork_object = pickle.loads(value)
        if isinstance(artwork_object, Artwork):
            self.logger.info("Received commission request")
            self.logger.info("Commission width: %f", artwork_object.width)
            self.logger.info("Commission height: %f", artwork_object.height)
            self.logger.info("Commission wait time: %s", artwork_object.wait_time)
            if not artwork_object.commission_complete:
                fragment = self.generate_piece(artwork_object)
                self.node.set(fragment.get_key(), pickle.dumps(fragment))

    async def connect_to_network(self):
        """
        Connect to the kademlia network.
        """
        self.node = self.kdm.network.Server(self.callback_function)
        await self.node.listen(self.port)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)


async def main():
    """Main function"""
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    port_num = sys.argv[1]
    if len(sys.argv) == 2:
        address = None
    else:
        address = int(sys.argv[2])
    peer = Peer(port_num, address, kademlia)
    await peer.connect_to_network()
    peer.commission_art_piece()


if __name__ == "__main__":
    asyncio.run(main())
