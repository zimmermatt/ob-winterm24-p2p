#!/usr/bin/env python3
"""Simple Test Module to set up a project structure.

Simple example/starter test module.
"""

from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import time
from threading import Thread
import unittest

from sample_module.udp_server import UdpServer


class UdpServerTest(unittest.TestCase):
    """Simple Test Class.

    Simple example/starter test class.
    """

    def test_message_is_cached(self):
        """Functional test to check whether messages can be sent over UDP to the server."""
        # this test has issues and should not be considered an example of a good test
        ip = "127.0.0.1"
        port = 64000
        server = UdpServer(ip, port)
        server_thread = Thread(target=server.serve)
        server_thread.start()
        time.sleep(0.1)  # give the server time to bind

        s = socket(AF_INET, SOCK_DGRAM)
        bytes_sent = s.sendto(b"Hello", (ip, port))
        self.assertGreater(bytes_sent, 0)
        s.sendto(b"shutdown", (ip, port))
        time.sleep(0.1)  # give the server time to close down
        server_thread.join()
        s.close()


if __name__ == "__main__":
    unittest.main()
