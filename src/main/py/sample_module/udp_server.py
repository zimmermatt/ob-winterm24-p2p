#!/usr/bin/env python3
"""Starter Module to set up a project structure.

Simple example/starter module that exports the `UdpServer` class.
"""

import logging
from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import sys


class UdpServer:
    """Simple UDP Server.

    Simple UDP Server that listens on UDP at a specified port for messages and caches it until the
    next message is recieved.
    """

    def __init__(self, server_ip: str, listen_port: int) -> None:
        """Construct a `UdpServer`.

        Parameters:
        server_ip   -- the ip to bind to
        listen_port -- the port to listen on
        """
        UdpServer.logger = logging.getLogger("UdpServer")
        self.ip = server_ip
        self.port = listen_port
        self.cached_message = ""

    def serve(self) -> None:
        """Bind to `ip` and `port` and listen for messages."""
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        address = (self.ip, self.port)
        UdpServer.logger.info("Binding to %r", address)
        udp_socket.bind(address)

        listen = True
        while listen:
            payload, address = udp_socket.recvfrom(512)
            UdpServer.logger.info('received message "%s" from %s', payload, address)
            self.cached_message = payload.decode("utf-8").strip()
            UdpServer.logger.info('cached message is "%s"', self.cached_message)
            shutdown = self.cached_message == "shutdown"
            UdpServer.logger.info("shutdown command = %s", shutdown)
            if shutdown:
                listen = False

        udp_socket.close()

    def get_cached_message(self) -> str:
        """Return the cached message"""
        return self.cached_message


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s | %(message)s", level=logging.INFO
    )
    udp_server = UdpServer("127.0.0.1", int(sys.argv[1]))
    udp_server.serve()
