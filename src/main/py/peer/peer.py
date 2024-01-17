#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""
import logging
import sys
import threading
from commission.artwork import Artwork

# join_ipfs_network, ipfs_publish, not implemented


class Peer:
    """
    Class to manage peer functionality.
    """

    logger = logging.getLogger("Peer")

    def __init__(self, network_address: str, port: int, ipfs) -> None:
        """
        Initialize the Peer class by joining the IPFS network.

        Params:
        - network_address (str): The network address to join.
        - port (int): The port number to use for the connection.
        """
        self.network_address = network_address
        self.port = port
        self.ipfs = ipfs
        self.commissions = []
        self.deadline_timers = {}

    def send_deadline_reached(self, commission: Artwork) -> None:
        """
        Mark the commission as complete, publish it on IPFS, and remove it from the list.
        """
        commission.set_complete()
        self.ipfs.ipfs_publish(commission.get_file_descriptor(), "Commission complete")
        self.commissions.remove(commission)

    def setup_deadline_timer(self, commission: Artwork) -> None:
        """
        Schedule the deadline notice for the commission.
        """
        deadline_seconds = commission.get_wait_time()
        deadline_timer = threading.Timer(
            deadline_seconds, self.send_deadline_reached, args=(commission,)
        )
        self.deadline_timers[commission.get_file_descriptor()] = deadline_timer
        deadline_timer.start()

    def send_commission_request(self, commission: Artwork) -> None:
        """
        Publish the commission on IPFS, add it to the list, and schedule the deadline notice.
        """
        self.ipfs.ipfs_publish(commission.get_file_descriptor(), commission)
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
                commission = Artwork(width, height, wait_time)
                self.send_commission_request(commission)
                break
            except ValueError:
                self.logger.error("Invalid input. Please enter a valid float.")

    def connect_to_network(self):
        """
        Connect to the IPFS network.
        """
        connected = self.ipfs.connect(self.network_address, self.port)
        if connected:
            self.logger.info(
                "Connected to %s running on port %d", self.network_address, self.port
            )
            return True
        self.logger.error("Failed to connect to %s", self.network_address)
        return False


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    address, port_num = sys.argv[1], int(sys.argv[2])
    # peer = Peer(address, port_num)
    # peer.connect_to_network()
    # peer.commission_art_piece()
