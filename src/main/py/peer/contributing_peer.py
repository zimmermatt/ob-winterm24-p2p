#!/usr/bin/env python3
"""
Module to manage peer functionality.

Peer class allows us to join the network, commission artwork, and generate fragments to share
"""
import asyncio
import logging
import sys
from server.network import NotifyingServer as kademlia
from peer.peer import Peer


# pylint: disable=too-many-instance-attributes
async def main():
    """Main function

    Run the file with the following:
    python3 peer.py <port_num> <key_filename> <address>
    """

    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    key_filename = sys.argv[2]
    port_num = int(sys.argv[1])
    if len(sys.argv) != 3:
        address = sys.argv[3]
    else:
        address = None
    peer = Peer(port_num, key_filename, address, kademlia)
    await peer.connect_to_network()


if __name__ == "__main__":
    asyncio.run(main())
