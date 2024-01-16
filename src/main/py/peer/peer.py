#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""

import threading
import time

def join_ipfs_network() -> None:
    """
    Dummy function to join the IPFS network.
    """
    # TODO: Implement joining IPFS network
    pass

def add_to_ipfs(commission) -> str:
    """
    Dummy function to add commission to IPFS and return file descriptor.
    """
    # TODO: Implement adding commission to IPFS
    return "file_descriptor"

def ipfs_publish(topic, message) -> None:
    """
    Dummy function to publish message on IPFS.
    """
    # TODO: Implement publishing message on IPFS
    pass

class Peer:
    """
    Class to manage peer functionality.
    """

    def __init__(self) -> None:
        """
        Initialize the Peer class by joining the IPFS network.
        """
        join_ipfs_network()
        self.commissions = []

    def create_commission(self, width: int, height: int, wait_time: int) -> dict:
        """
        Create a commission dictionary and add it to IPFS.
        Return the commission dictionary.
        """
        commission = {
            "width": width,
            "height": height,
            "wait_time": wait_time,
            "commission_complete": False,
        }
        ipfs_file_descriptor = add_to_ipfs(commission)
        commission['ipfs_file_descriptor'] = ipfs_file_descriptor
        return commission
    
    def send_deadline_notice(self, commission: dict) -> None:
        """
        Mark the commission as complete, publish it on IPFS, and remove it from the list.
        """
        commission['commission_complete'] = True
        ipfs_publish(commission)
        self.commissions.remove(commission)

    def send_commission_request(self, commission: dict) -> None:
        """
        Publish the commission on IPFS, add it to the list, and schedule the deadline notice.
        """
        ipfs_publish(commission)
        current_time = int(time.time())
        deadline_seconds = current_time + commission['wait_time']
        self.commissions.append(commission)
        deadline_timer = threading.Timer(deadline_seconds, self.send_deadline_notice, args=(commission,))
        deadline_timer.start()

    def commission_art_piece(self) -> None:
        """
        Get commission details from user input, create a commission, and send the request.
        """
        width = int(input("Enter commission width: "))
        height = int(input("Enter commission height: "))
        wait_time = int(input("Enter wait time in seconds: "))
        commission = self.create_commission(width, height, wait_time)
        self.send_commission_request(commission)

        