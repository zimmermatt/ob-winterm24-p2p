#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""
import time
import asyncio
from datetime import timedelta
import hashlib
import ipaddress
import pickle
import logging
import sys
from PIL import Image
from server.network import NotifyingServer as kademlia
from commission.artfragment import ArtFragment
from commission.artwork import Artwork
from commission.artfragmentgenerator import generate_fragment
from peer.ledger import Ledger
from peer.inventory import Inventory
from peer.wallet import Wallet
from exchange.offer_response import OfferResponse
from exchange.offer_announcement import OfferAnnouncement
from drawing.drawing import Constraint
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
        else:
            self.network_port_num = None
            self.network_ip_address = None
        self.port = port
        self.keys = {}
        with open(f"{key_filename}.pub", "r", encoding="utf-8") as public_key_file:
            self.keys["public"] = public_key_file.read()
        with open(key_filename, "r", encoding="utf-8") as private_key_file:
            self.keys["private"] = private_key_file.read()
        self.kdm = kdm
        self.node = None
        self.commission_requests_received = []
        self.gui_callback = None
        self.inventory = Inventory()
        self.ledger = Ledger()
        self.wallet = Wallet()

    async def send_deadline_reached(self, commission: Artwork) -> None:
        """
        Mark the commission as complete, publish it on kademlia, and remove it from the list.
        """

        commission.set_complete()
        commission.ledger.add_owner(self.keys["public"])
        try:
            set_success = await self.node.set(
                commission.get_key(), pickle.dumps(commission)
            )
            if set_success:
                self.logger.info("Commission complete")
            else:
                self.logger.error("Commission failed to complete")
            self.inventory.add_owned_artwork(commission)
            self.inventory.commission_canvases[commission.key].save(
                "pics/canvas13.png", "PNG"
            )
            self.inventory.remove_commission(commission)
        except TypeError:
            self.logger.info(commission)
            self.logger.error("Commission type is not pickleable")

    async def setup_deadline_timer(self, commission: Artwork) -> None:
        """
        Schedule the deadline notice for the commission.
        """

        deadline_seconds = commission.get_remaining_time()
        utils.call_later()(
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
            self.logger.info(commission)
            self.logger.error("Commission type is not pickleable")

    async def commission_art_piece(
        self, width=None, height=None, wait_time=None, palette_limit=None
    ) -> None:
        """
        Get commission details from user input, create a commission, and send the request.
        """

        while True:
            try:
                width = float(input("Enter commission width: ")) if not width else width
                height = (
                    float(input("Enter commission height: ")) if not height else height
                )
                palette_limit = (
                    float(input("Enter palette limit: "))
                    if not palette_limit
                    else palette_limit
                )
                wait_time = (
                    float(input("Enter wait time in seconds: "))
                    if not wait_time
                    else wait_time
                )
                constraint = Constraint(palette_limit, "any")
                commission = Artwork(
                    width,
                    height,
                    timedelta(seconds=wait_time),
                    self.ledger,
                    constraint=constraint,
                    originator_public_key=self.keys["public"],
                    originator_long_id=self.node.node.long_id,
                )
                await self.send_commission_request(commission)
                self.inventory.add_commission(commission)
                self.inventory.commission_canvases[commission.key] = Image.new(
                    "RGBA",
                    (int(commission.width), int(commission.height)),
                    (0, 0, 0, 0),
                )
                return commission
            except ValueError:
                self.logger.error("Invalid input. Please enter a valid float.")

    async def handle_exchange_announcement_deadline(
        self,
        announcement_type: str,
        announcement_key,
        offer_announcement: OfferAnnouncement,
    ):
        """Handle the deadline for an exchange announcement"""

        self.inventory.remove_pending_exchange(announcement_key)
        self.inventory.completed_exchanges.add(announcement_key)

        self.wallet.add_to_balance(offer_announcement.get_price())
        self.logger.info("Exchange announcement deadline reached")

        try:
            set_success = await self.node.set(
                announcement_key, pickle.dumps(offer_announcement)
            )
            if set_success:
                self.logger.info("%s announced", announcement_type)
            else:
                self.logger.error("%s failed to announce", announcement_type)
        except TypeError:
            self.logger.error("%s type is not pickleable", announcement_type)

    async def announce_exchange(
        self,
        exchange_type: str,
        price: int,
        wait_time=timedelta(seconds=10),
    ):
        """
        Announce an exchange to the network.
        """

        if exchange_type not in ("sale", "trade"):
            self.logger.error("Invalid exchange type")
            return

        self.logger.info("Announcing exchange")
        artwork = self.inventory.get_artwork_to_exchange()
        if not artwork:
            self.logger.info("No artwork for exchange")
            return

        offer_announcement = OfferAnnouncement(artwork, price, exchange_type)

        announcement_key = utils.generate_random_sha1_hash()
        self.inventory.add_pending_exchange(announcement_key, offer_announcement)

        asyncio.get_event_loop().call_later(
            wait_time.total_seconds(),
            asyncio.create_task,
            self.handle_exchange_announcement_deadline(
                exchange_type, announcement_key, offer_announcement
            ),
        )

        try:
            set_success = await self.node.set(
                announcement_key, pickle.dumps(offer_announcement)
            )
            if set_success:
                self.logger.info("%s announced", exchange_type)
            else:
                self.logger.error("%s failed to announce", exchange_type)
        except TypeError:
            self.logger.error("%s type is not pickleable", exchange_type)

    async def send_exchange_response(
        self, exchange_key: bytes, announcement: OfferAnnouncement
    ):
        """
        Send a exchange response to the network.
        """

        if announcement.originator_public_key == self.keys["public"]:
            return

        if announcement.get_exchange_type() == "trade":
            if (
                exchange_key in self.inventory.pending_exchanges
                and announcement.deadline_reached
            ):
                self.inventory.remove_pending_exchange(exchange_key)
                return
        if announcement.get_exchange_type() == "sale":
            if announcement.deadline_reached:
                return
            if self.wallet.get_balance() < announcement.get_price():
                self.logger.info("Insufficient funds.")
                return

        self.logger.info(
            "Sending %s response to %s",
            announcement.get_exchange_type(),
            announcement.originator_public_key,
        )

        if announcement.get_exchange_type() == "trade":
            artwork_to_exchange = self.inventory.get_artwork_to_exchange()
            if not artwork_to_exchange:
                self.logger.info("No artwork to send")
                return
        offer_response = (
            OfferResponse(
                exchange_key,
                artwork_to_exchange,
                announcement.get_price(),
                self.keys["public"],
            )
            if announcement.get_exchange_type() == "trade"
            else OfferResponse(
                exchange_key, None, announcement.get_price(), self.keys["public"]
            )
        )

        response_key = utils.generate_random_sha1_hash()

        try:
            set_success = await self.node.set(
                response_key, pickle.dumps(offer_response)
            )
            if set_success:
                self.logger.info("%s response sent", announcement.get_exchange_type())
            else:
                self.logger.error(
                    "%s response failed to send", announcement.get_exchange_type()
                )

        except TypeError:
            self.logger.error(
                "%s response type is not pickleable", announcement.get_exchange_type()
            )

    async def handle_exchange_response(
        self,
        exchange_key: bytes,
        response: OfferResponse,
    ):
        """
        Handle an exchange response from the network.
        """

        self.logger.info("Handling exchange response")
        if exchange_key in self.inventory.pending_exchanges:
            self.inventory.remove_pending_exchange(exchange_key)
            await self.handle_accept_exchange(response)
            self.logger.info("Exchange successful")
        else:
            await self.handle_reject_exchange(response)
            self.logger.info("Exchange unsuccessful")

    async def handle_accept_exchange(
        self,
        response: OfferResponse,
    ):
        """Handle an accepted exchange"""

        self.wallet.remove_from_balance(response.get_price())
        exchanger = response.get_exchanger_public_key()
        self.ledger.add_owner(exchanger)
        self.logger.info("%s accepted the exchange.", exchanger)

    async def handle_reject_exchange(self, response: OfferResponse):
        """Handle a rejected exchange"""

        self.logger.info(
            "%s rejected the exchange.", response.get_exchanger_public_key()
        )

    async def contribute_to_artwork(self, message_object: Artwork):
        """
        Contribute to an artwork by generating a fragment and sending it to the network.
        """
        fragment = generate_fragment(
            message_object,
            message_object.originator_long_id,
            self.keys["public"],
            self.node.node.long_id,
        )
        try:
            set_success = await self.node.set(
                utils.generate_random_sha1_hash(), pickle.dumps(fragment)
            )
            if set_success:
                self.logger.info("Fragment sent")
            else:
                self.logger.error("Fragment failed to send")
        except TypeError:
            self.logger.error("Fragment type is not pickleable")

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
            if (
                not message_object.commission_complete
                and message_object.originator_public_key != self.keys["public"]
            ):
                self.commission_requests_received.append(message_object)
                if callable(self.gui_callback):
                    self.gui_callback()  # pylint: disable=not-callable
                else:
                    await self.contribute_to_artwork(message_object)
        elif isinstance(message_object, ArtFragment):
            if message_object.artwork_id in self.inventory.commissions:
                self.inventory.commissions[
                    message_object.artwork_id
                ] = self.merge_canvas(
                    message_object,
                    self.inventory.commission_canvases[message_object.artwork_id],
                )
        elif isinstance(message_object, OfferAnnouncement):
            self.logger.info("Received exchange announcement")
            await self.send_exchange_response(key, message_object)
        elif isinstance(message_object, OfferResponse):
            self.logger.info("Received exchange response")
            await self.handle_exchange_response(key, message_object)
        else:
            self.logger.error("Invalid object received")

    async def connect_to_network(self, wait_time=0):
        """
        Connect to the kademlia network.
        """

        self.node = self.kdm(
            self.data_stored_callback,
            node_id=hashlib.sha1(self.keys["public"].encode()).digest(),
        )
        await self.node.listen(self.port)
        time.sleep(wait_time)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)

    def merge_canvas(self, fragment: ArtFragment, canvas) -> Image.Image:
        """
        Merge fragments received from a Contributor Artist Peer into a complete colored canvas
        """
        pixels = canvas.load()

        for pixel in fragment.pixels:
            pixels[pixel.coordinates.x, pixel.coordinates.y] = pixel.color

        return canvas

    async def create_new_ledger_entry(self) -> Ledger:
        """
        Create a new ledger for the artwork
        """

        add = await self.ledger.add_owner(self.keys["public"])
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
    await peer.connect_to_network(15)
    time.sleep(10)
    await peer.commission_art_piece()
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
