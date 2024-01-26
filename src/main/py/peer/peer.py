#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""
import asyncio
from datetime import timedelta
import hashlib
import ipaddress
import pickle
import logging
import sys
import server as kademlia
from commission.artwork import Artwork


class Peer:
    """Class to manage peer functionality"""

    logger = logging.getLogger("Peer")

    def __init__(
        self,
        port: int,
        key_filename: str,
        peer_network_address: str,
        kdm,
    ) -> None:
        """
        Initialize the Peer class by joining the kademlia network.

        Params:
        - port (int): The port number for the peer to listen on.
        - public_key_filename (str): The filename of the public key.
        - private_key_filename (str): The filename of the private key.
        - peer_network_address (str): String containing the IP address and port number of a peer
          on the network separated by a colon.
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
        with open(f"{key_filename}.pub", "r", encoding="utf-8") as public_key_file:
            self.public_key = public_key_file.read()
        with open(key_filename, "r", encoding="utf-8") as private_key_file:
            self.private_key = private_key_file.read()
        self.kdm = kdm
        self.node = None

    async def send_deadline_reached(self, commission: Artwork) -> None:
        """
        Mark the commission as complete, publish it on kademlia, and remove it from the list.
        """

        commission.set_complete()
        try:
            set_success = await self.node.set(
                commission.get_key(), pickle.dumps(commission)
            )
            if set_success:
                self.logger.info("Commission complete")
            else:
                self.logger.error("Commission failed to complete")
        except TypeError:
            self.logger.error("Commission type is not pickleable")

    async def setup_deadline_timer(self, commission: Artwork) -> None:
        """
        Schedule the deadline notice for the commission.
        """

        deadline_seconds = commission.get_remaining_time()
        asyncio.get_event_loop().call_later(
            deadline_seconds,
            asyncio.create_task,
            self.send_deadline_reached(commission),
        )

    async def send_commission_request(self, commission: Artwork) -> None:
        """
        Publish the commission on kademlia, add it to the list, and schedule the deadline notice.
        """

        try:
            set_success = await self.node.set(
                commission.get_key(), pickle.dumps(commission)
            )
            if set_success:
                self.logger.info("Commission sent")
            else:
                self.logger.error("Commission failed to send")
            await self.setup_deadline_timer(commission)
        except TypeError:
            self.logger.error("Commission type is not pickleable")

    async def commission_art_piece(self) -> None:
        """
        Get commission details from user input, create a commission, and send the request.
        """

        while True:
            try:
                width = float(input("Enter commission width: "))
                height = float(input("Enter commission height: "))
                wait_time = float(input("Enter wait time in seconds: "))
                commission = Artwork(
                    width,
                    height,
                    timedelta(seconds=wait_time),
                    originator_public_key=self.public_key,
                )
                await self.send_commission_request(commission)
                return commission
            except ValueError:
                self.logger.error("Invalid input. Please enter a valid float.")

    def generate_fragment(self, commission: Artwork):
        """Generate a piece of the artwork"""

        self.logger.info("Generating fragment")
        return commission

    async def data_stored_callback(self, key, value):
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
                fragment = self.generate_fragment(artwork_object)
                try:
                    set_success = await self.node.set(
                        fragment.get_key(), pickle.dumps(fragment)
                    )
                    if set_success:
                        self.logger.info("Fragment sent")
                    else:
                        self.logger.error("Fragment failed to send")
                except TypeError:
                    self.logger.error("Fragment type is not pickleable")
        else:
            self.logger.error("Invalid object received")

    async def connect_to_network(self):
        """
        Connect to the kademlia network.
        """

        self.node = self.kdm.network.NotifyingServer(
            self.data_stored_callback,
            node_id=hashlib.sha1(self.public_key.encode()).digest(),
        )
        await self.node.listen(self.port)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)

    def add_to_art_collection(self, artwork, collection):
        """
        Add artwork to collection
        """

        try:
            collection.add_to_art_collection(artwork)
            logging.info("Artwork successfully added to collection.")
        except ValueError as e:
            logging.error("Failed to add artwork to collection: %s", e)

    def remove_from_art_collection(self, artwork, collection):
        """
        Remove artwork from collection
        """

        try:
            collection.remove_from_art_collection(artwork)
            logging.info("Artwork removed from collection successfully.")
        except ValueError as e:
            logging.error("Failed to remove artwork from collection: %s", e)

    def swap_art(self, my_art, their_art, my_art_collection, their_art_collection):
        """
        Swap artwork between two collections
        """

        try:
            if (
                my_art in my_art_collection.get_artworks()
                and their_art in their_art_collection.get_artworks()
            ):
                my_art_collection.remove_from_art_collection(my_art)
                their_art_collection.remove_from_art_collection(their_art)
                my_art_collection.add_to_art_collection(their_art)
                their_art_collection.add_to_art_collection(my_art)
                logging.info("Artwork successfully swapped.")
            else:
                logging.warning("Artwork not found in collections.")
        except ValueError as e:
            logging.error("Failed to swap artwork: %s", e)


async def main():
    """Main function

    Run the file with the following:
    python3 peer.py <port_num> <key_filename> <address>
    """

    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    port_num = sys.argv[1]
    key_filename = sys.argv[2]
    if len(sys.argv) == 3:
        address = None
    else:
        address = sys.argv[2]
    peer = Peer(port_num, key_filename, address, kademlia)
    await peer.connect_to_network()
    await peer.commission_art_piece()


if __name__ == "__main__":
    asyncio.run(main())
