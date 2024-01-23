#!/usr/bin/env python3

"""
Test Module for the Protocol class
"""

import unittest
import asyncio
import hashlib

from unittest.mock import Mock
from server.network import NewServer


class TestNewServer(unittest.IsolatedAsyncioTestCase):
    """Test class for NewServer class"""

    def setUp(self):
        """Create instances of NewServer"""
        self.mock_store_callback = Mock()

        self.node1 = NewServer(self.mock_store_callback)
        self.node2 = NewServer(self.mock_store_callback)

    def test_init(self):
        """Test the __init__ method of NewServer"""
        self.assertEqual(self.node1.store_callback, self.mock_store_callback)

    async def test_store(self):
        """Test the store method of NewServer"""
        await self.node1.listen(8468)
        await self.node2.listen(8469)
        await self.node2.bootstrap([("127.0.0.1", 8468)])

        key = "key"
        key_hash = hashlib.sha1(key.encode()).digest()

        await self.node1.set("key", "value")
        self.mock_store_callback.assert_called_with(key_hash, "value")
        self.node1.stop()
        self.node2.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    async def run_async_tests():
        """Run the tests."""
        await unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))

    result = loop.run_until_complete(run_async_tests())
    loop.close()
