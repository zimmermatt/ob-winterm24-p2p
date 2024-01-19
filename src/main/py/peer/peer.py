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
import kademlia
import random
from PIL import Image
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

    async def connect_to_network(self):
        """
        Connect to the kademlia network.
        """
        self.node = self.kdm.network.Server()
        await self.node.listen(self.port)
        if self.network_ip_address is not None:
            await self.node.bootstrap(
                [(str(self.network_ip_address), self.network_port_num)]
            )
        self.logger.info("Running server on port %d", self.port)

    def merge_canvas(width: int, height: int, fragments) -> Image.Image:
        """
        Merge fragments received from Contributor Artists Peer into a completed canvas with colored pixels and save them
        """
        canvas = Image.new(mode="RGB", size=(width, height), color=(255,255,255))
        pixels = canvas.load()

        for i in range(len(fragments)):
            x = fragments[i][0]
            y = fragments[i][1]
            # Making them black for now
            pixels[x, y] = (0, 0, 0)

        canvas.save("canvas.png", "PNG")
        return canvas

    def generate_fragments(constraints):
        """
        Generate fragments as a list of (x,y) tuples coordinates of the pixels to be colored from the constraints tuples. For now, constraints only have width and height.
        """
        random.seed(7)
        # We're going to generate fragments by choosing the starting coordinate, and then the width and height of the fragment to make a rectangle.
        # We're going to only make the pixels within that rectangle be colored
        x = random.randint(0, constraints[0] - 1)
        y = random.randint(1, constraints[1] - 1)

        colored_pixels = []

        w_fragment = random.randint(x, constraints[0] - x - 1)
        h_fragment = random.randint(y, constraints[1] - y - 1)

        #Means that currently 0.3 of the fragment will be colored
        for i in range(int(w_fragment * h_fragment * 0.3)):
            x_pixel = random.randint(x, x + w_fragment - 1)
            y_pixel = random.randint(y, y + h_fragment - 1)
            colored_pixels.append((x_pixel, y_pixel))

        return colored_pixels


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
