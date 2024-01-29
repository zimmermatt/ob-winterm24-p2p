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
from PIL import Image
from server.network import NotifyingServer as kademlia
from commission.artwork import Artwork
from peer.ledger import Ledger
from peer.inventory import Inventory
from trade.offer_response import OfferResponse
from trade.offer_announcement import OfferAnnouncement
from trade.trade_confirmation import TradeConfirmation
import utils


# pylint: disable=too-many-instance-attributes
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
        - key_filename (str): The filename of the private key.
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
        self.keys = {}
        with open(f"{key_filename}.pub", "r", encoding="utf-8") as public_key_file:
            self.keys["public"] = public_key_file.read()
        with open(key_filename, "r", encoding="utf-8") as private_key_file:
            self.keys["private"] = private_key_file.read()
        self.kdm = kdm
        self.node = None
        self.inventory = Inventory()
        self.ledger = Ledger()

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
            self.inventory.add_owned_artwork(commission)
            self.inventory.remove_commission(commission)
        except TypeError:
            self.logger.error("Commission type is not pickleable")

    async def setup_deadline_timer(self, commission: Artwork) -> None:
        """
        Schedule the deadline notice for the commission.
        """

        deadline_seconds = commission.get_remaining_time()
        asyncio.get_event_loop().call_later(
            deadline_seconds,
            await self.send_deadline_reached(commission),
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
                    self.ledger,
                    originator_public_key=self.keys["public"],
                )
                await self.send_commission_request(commission)
                self.inventory.add_commission(commission)
                return commission
            except ValueError:
                self.logger.error("Invalid input. Please enter a valid float.")

    def generate_fragment(self, commission: Artwork):
        """Generate a piece of the artwork"""

        self.logger.info("Generating fragment")
        return commission

    async def handle_announcement_deadline(
        self, announcement_key, offer_announcement: OfferAnnouncement
    ):
        """Handle the deadline for an announcement"""

        self.inventory.remove_pending_trade(announcement_key)
        self.inventory.completed_trades.add(announcement_key)
        offer_announcement.deadline_reached = True
        try:
            set_success = await self.node.set(
                announcement_key, pickle.dumps(offer_announcement)
            )
            if set_success:
                self.logger.info("Trade announced")
            else:
                self.logger.error("Trade failed to announce")
        except TypeError:
            self.logger.error("Trade type is not pickleable")

    async def announce_trade(self, wait_time=timedelta(seconds=10)):
        """
        Announce a trade to the network.
        """

        self.logger.info("Announcing trade")
        artwork = self.inventory.get_artwork_to_trade()
        if not artwork:
            self.logger.info("No artwork to trade")
            return
        offer_announcement = OfferAnnouncement(artwork)
        announcement_key = utils.generate_random_sha1_hash()
        self.inventory.add_pending_trade(announcement_key, offer_announcement)
        asyncio.get_event_loop().call_later(
            wait_time,
            asyncio.create_task,
            self.handle_announcement_deadline(announcement_key, offer_announcement),
        )
        try:
            set_success = await self.node.set(
                announcement_key, pickle.dumps(offer_announcement)
            )
            if set_success:
                self.logger.info("Trade announced")
            else:
                self.logger.error("Trade failed to announce")
        except TypeError:
            self.logger.error("Trade type is not pickleable")

    async def send_trade_response(
        self, trade_id: bytes, announcement: OfferAnnouncement
    ):
        """
        Send a trade response to the network.
        """

        if announcement.originator_public_key == self.keys["public"]:
            return
        if trade_id in self.inventory.pending_trades and announcement.deadline_reached:
            self.inventory.remove_pending_trade(trade_id)
            return
        self.logger.info(
            "Sending trade response to %s", announcement.originator_public_key
        )
        artwork_to_trade = self.inventory.get_artwork_to_trade()
        if not artwork_to_trade:
            self.logger.info("No trade response to send")
            return
        offer_response = OfferResponse(
            trade_id, artwork_to_trade.key, self.keys["public"]
        )
        response_key = utils.generate_random_sha1_hash()
        self.inventory.add_pending_trade(
            trade_id,
            offer_response,
        )
        try:
            set_success = await self.node.set(
                response_key, pickle.dumps(offer_response)
            )
            if set_success:
                self.logger.info("Trade response sent")
            else:
                self.logger.error("Trade response failed to send")
        except TypeError:
            self.logger.error("Trade response type is not pickleable")

    async def handle_accept_trade(self, response: OfferResponse):
        """Handle an accepted trade"""

        trade_confirmation = TradeConfirmation(
            response.trade_id,
            self.inventory.pending_trades[response.trade_id].get_artwork_key(),
            self.keys["public"],
            True,
        )
        try:
            set_success = await self.node.set(
                utils.generate_random_sha1_hash(), pickle.dumps(trade_confirmation)
            )
            if set_success:
                self.logger.info("Fragment sent")
                self.inventory.remove_owned_artwork(
                    self.inventory.pending_trades[response.trade_id].get_artwork_key()
                )
                # ledger update here for our owned artwork
                # update the artwork in the dht with a set
                artwork_received = self.node.get(response.offer_id)
                self.inventory.add_owned_artwork(artwork_received)
                # ledger update here for other artwork
                # update the artwork in the dht with a set
            else:
                self.logger.error("Fragment failed to send")
        except TypeError:
            self.logger.error("Fragment type is not pickleable")

    async def handle_reject_trade(self, response: OfferResponse):
        """Handle a rejected trade"""

        trade_confirmation = TradeConfirmation(
            response.trade_id,
            self.inventory.pending_trades[response.trade_id].get_artwork_key(),
            self.keys["public"],
            False,
        )
        try:
            set_success = await self.node.set(
                utils.generate_random_sha1_hash(), pickle.dumps(trade_confirmation)
            )
            if set_success:
                self.logger.info("Fragment sent")
            else:
                self.logger.error("Fragment failed to send")
        except TypeError:
            self.logger.error("Fragment type is not pickleable")

    async def handle_trade_response(self, trade_id: bytes, response: OfferResponse):
        """
        Handle a trade response from the network.
        """

        self.logger.info("Handling trade response")
        if trade_id in self.inventory.pending_trades:
            self.inventory.remove_pending_trade(trade_id)
            if response.trade_id in self.inventory.pending_trades:
                self.inventory.remove_pending_trade(response.trade_id)
            self.handle_accept_trade(response)
            self.logger.info("Trade successful")
        else:
            self.handle_reject_trade(response)

    async def data_stored_callback(self, key, value):
        """
        Callback function for when data is stored.
        Args:
            key (bytes): The key to store.
            value (bytes): The value to store.
        """

        self.logger.info("Data stored with key: %s", key)
        self.logger.info("Data stored with value: %s", value)
        message_object = pickle.loads(value)
        if isinstance(message_object, Artwork):
            self.logger.info("Received commission request")
            if not message_object.commission_complete:
                fragment = self.generate_fragment(message_object)
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
        elif isinstance(message_object, OfferAnnouncement):
            self.logger.info("Received trade announcement")
            await self.send_trade_response(key, message_object)
        elif isinstance(message_object, OfferResponse):
            self.logger.info("Received trade response")
            await self.handle_trade_response(key, message_object)
        elif isinstance(message_object, TradeConfirmation):
            self.logger.info("Received trade confirmation")
            if (
                message_object.accepted
                and message_object.trade_id in self.inventory.pending_trades
            ):
                self.logger.info("exchange ownership")
                self.inventory.remove_pending_trade(message_object.trade_id)
                self.inventory.completed_trades.add(message_object.trade_id)
                self.inventory.add_owned_artwork(message_object.announced_offer_id)
                self.inventory.remove_owned_artwork(message_object.responded_offer_id)
            else:
                self.logger.info("trade failed")
        else:
            self.logger.error("Invalid object received")

    async def connect_to_network(self):
        """
        Connect to the kademlia network.
        """

        self.node = self.kdm(
            self.data_stored_callback,
            node_id=hashlib.sha1(self.keys["public"].encode()).digest(),
        )
        await self.node.listen(self.port)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)

    def merge_canvas(self, width: int, height: int, fragment) -> Image.Image:
        """
        Merge fragments received from a Contributor Artist Peer into a complete colored canvas
        """
        canvas = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
        pixels = canvas.load()

        for pixel in fragment:
            x = pixel[0][0]
            y = pixel[0][1]
            # Making them black for now
            pixels[x, y] = fragment.get_fragment_color()

        canvas.save("canvas.png", "PNG")
        return canvas

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

    async def create_new_ledger_entry(self) -> Ledger:
        """
        Create a new ledger for the artwork
        """

        add = await self.ledger.add_owner(self)
        if not add:
            self.logger.error("Failed to add owner to ledger")
            return
        return add


async def main():
    """Main function

    Run the file with the following:
    python3 peer.py <port_num> <key_filename> <address>
    """

    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    port_num = int(sys.argv[1])
    key_filename = sys.argv[2]
    if len(sys.argv) == 3:
        address = None
    else:
        address = sys.argv[3]
    peer = Peer(port_num, key_filename, address, kademlia)
    await peer.connect_to_network()
    # await peer.commission_art_piece()


if __name__ == "__main__":
    asyncio.run(main())
