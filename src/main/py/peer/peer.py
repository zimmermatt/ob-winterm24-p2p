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
import server as kademlia
from commission.artwork import Artwork
from commission.artcollection import TradeStatus, ArtCollection

# create the pending list


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
        self.art_collection = ArtCollection()

    async def send_deadline_reached(self, commission: Artwork) -> None:
        """
        Mark the commission as complete, publish it on kademlia, and remove it from the list.
        """

        # handle cases when commission can't be pickekd

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
        deadline_timer = asyncio.get_event_loop().call_later(
            deadline_seconds,
            asyncio.create_task,
            self.send_deadline_reached(commission),
        )
        self.deadline_timers[commission.get_key()] = deadline_timer

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
                self.commissions.append(commission)
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
                commission = Artwork(width, height, timedelta(seconds=wait_time))
                await self.send_commission_request(commission)
                break
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

        self.node = self.kdm.network.NotifyingServer(self.data_stored_callback)
        await self.node.listen(self.port)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)

    def send_trade_status(self, commission: ArtCollection, status: TradeStatus):
        """
        Send the trade status to the commission.
        """

        self.logger.info("Sending trade status: %s", status)
        self.art_collection.set_trade_status(commission, status)

    def receive_trade_status(self, commission: ArtCollection):
        """
        Receive the trade status from the commission.
        """

        self.logger.info("Sending trade received notice")
        self.art_collection.set_trade_status(commission, TradeStatus.RECEIVED)

    def accepted_trade_handling(self, commission: ArtCollection):
        """
        Accept the trade.
        """

        self.logger.info("Handle trade acceptance")
        commission.trade_accepted(self)

    def rejected_trade_handling(self, commission: ArtCollection):
        """
        Reject the trade.
        """

        self.logger.info("Handle trade rejection")
        commission.trade_rejected(self)

    def complete_received_trade(self, commission: ArtCollection):
        """
        Update the trade status to completed.
        """

        self.logger.info("Sending trade complete notice")

        commission.set_trade_status(TradeStatus.COMPLETED)

    def get_trade_status(self, commission: ArtCollection):
        """
        Get the trade status for the commission.
        """

        self.logger.info("Getting trade status")
        return self.art_collection.get_trade_status(commission)

    def set_trade_status(self, commission: ArtCollection, status: TradeStatus):
        """
        Set the trade status for the commission.
        """

        self.logger.info("Setting trade status")
        self.art_collection.set_trade_status(commission, status)

    def swap_art(self, other_peer, my_art: ArtCollection, their_art: ArtCollection):
        """
        Swap my_art from this peer's collection with their_art from other_peer's collection.
        """

        # handle when art isn't in the collection

        self.logger.info("Swapping %s with %s's %s", my_art, other_peer, their_art)

        self.remove_from_art_collection(my_art)
        other_peer.add_to_art_collection(my_art)

        other_peer.remove_from_art_collection(their_art)
        self.add_to_art_collection(their_art)

    def add_to_art_collection(self, commission: ArtCollection):
        """
        Add the commission to the art collection.
        """

        self.logger.info("Adding commission to art collection")
        self.art_collection.add_artwork(commission)

    def remove_from_art_collection(self, commission: ArtCollection):
        """
        Remove the commission from the art collection.
        """

        self.logger.info("Removing commission from art collection")
        self.art_collection.remove_artwork(commission)


async def main():
    """Main function"""

    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    port_num = sys.argv[1]
    if len(sys.argv) == 2:
        address = None
    else:
        address = sys.argv[2]
    peer = Peer(port_num, address, kademlia)
    await peer.connect_to_network()
    await peer.commission_art_piece()


if __name__ == "__main__":
    asyncio.run(main())
