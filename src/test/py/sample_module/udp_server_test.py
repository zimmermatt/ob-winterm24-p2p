#!/usr/bin/env python3
"""Simple Test Module to set up a project structure.

Simple example/starter test module.
"""

import unittest

from sample_module.udp_server import UdpServer


class UdpServerTest(unittest.TestCase):
    """Simple Test Class.

    Simple example/starter test class.
    """

    # Favoring self documenting test method names
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.server = UdpServer("127.0.0.1", 64000)

    def test_message_is_cached(self):
        self.server.handle(b"Hello")
        self.assertEqual(self.server.get_cached_message(), "Hello")

    def test_non_shutdown_message_does_not_return_the_shutdown_flag(self):
        self.assertFalse(self.server.handle(b"Hello"))

    def test_shutdown_message_returns_the_shutdown_flag(self):
        self.assertTrue(self.server.handle(b"shutdown"))

    def test_invalid_payload_does_not_throw_and_cache_is_maintained(self):
        self.server.handle(b"Hello")
        self.server.handle(bytes("incompatible payload", "utf-16"))
        self.assertEqual(self.server.get_cached_message(), "Hello")


if __name__ == "__main__":
    unittest.main()
