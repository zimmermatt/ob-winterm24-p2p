#!/usr/bin/env python3
"""
Test Module for the Peer class
"""

import asyncio
from datetime import timedelta
import logging
import pickle
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from commission.artwork import Artwork
from ledger.ledger import Ledger
from peer.peer import Peer


class MockNode:
    """
    A mock implementation of the Node class.
    """

    def __init__(self):
        """Initializes an instance of the MockNode class."""
        self.data_store = {}

    async def set(self, key, value):
        """Stores a value based on the key."""
        self.data_store[key] = value

    def get(self, key):
        """Returns a value based on the key."""
        if key in self.data_store:
            return self.data_store[key]
        raise KeyError(f"No value found for key: {key}")

    async def bootstrap(self, peers):
        """Bootstrap the node with a peer."""
        if len(peers) > 0:
            return True
        return False

    async def listen(self, port):
        """Listen on the port."""
        if port > 0:
            return True
        return False


class TestPeer(unittest.IsolatedAsyncioTestCase):
    """
    Class to test peer functionality.
    """

    # pylint: disable=too-many-instance-attributes

    test_logger = logging.getLogger("TestPeer")

    def setUp(self):
        """
        Initialize Kademlia Mocks and Peer instance
        """

        self.mock_kdm = MagicMock()
        self.mock_node = AsyncMock(spec=MockNode)
        self.mock_kdm.network.NotifyingServer.return_value = self.mock_node
        self.peer = Peer(
            5001,
            "src/test/py/resources/peer_test",
            "127.0.0.1:5000",
            self.mock_kdm,
        )
        self.deadline_task = None
        self.ledger = Ledger()
        self.artwork1 = Artwork(10, 10, timedelta(minutes=10), self.ledger)
        self.artwork2 = Artwork(10, 10, timedelta(minutes=10), self.ledger)
        self.peer2 = Peer(
            8000, "src/test/py/resources/peer_test", "127.0.0.1:5000", self.mock_kdm
        )

    def test_initialization(self):
        """
        Test case to verify the initialization of the Peer class.
        """
        # Verify that the network address is set to "127.0.0.1"
        self.assertEqual(str(self.peer.network_ip_address), "127.0.0.1")
        # Verify that the port is set to 5001
        self.assertEqual(self.peer.port, 5001)
        # Verify that the kdm instance is set to the mock_kdm object
        self.assertEqual(self.peer.kdm, self.mock_kdm)

    async def test_connect(self):
        """
        Test case for connecting to the network.
        """
        await self.peer.connect_to_network()
        self.peer.node.bootstrap.assert_called_once()

    @patch("builtins.input", side_effect=["10", "20", "10"])
    async def test_commission_art_piece(self, mock_input):
        """
        Test case for the commission_art_piece method of the Peer class.
        This test verifies that the commission_art_piece method correctly adds a commission,
        publishes it on Kademlia, and schedules and sends a deadline notice.
        """
        with patch(
            "asyncio.get_event_loop",
            return_value=MagicMock(
                call_later=lambda *args: setattr(
                    self, "deadline_task", asyncio.create_task(args[2])
                )
            ),
        ):
            self.test_logger.debug(mock_input)
            self.peer.node = self.mock_node
            commission = await self.peer.commission_art_piece()
            self.mock_node.set.assert_called_with(
                commission.get_key(), pickle.dumps(commission)
            )
            self.assertEqual(commission.width, 10)
            self.assertEqual(commission.height, 20)
            self.assertLessEqual(commission.wait_time, timedelta(seconds=10))
            # Check that send_deadline_reached was called, which in turn calls our node's set method
            await self.deadline_task
            self.assertEqual(self.mock_node.set.call_count, 2)

    def test_add_to_art_collection(self):
        """
        Test case for the add_to_art_collection method of the Peer class.
        This test verifies that the add_to_art_collection method correctly adds an artwork
        """

        self.peer.add_to_art_collection(self.artwork1, self.peer2)
        self.assertIn(self.artwork1, self.peer2.art_collection.artworks)
        self.assertIn(self.peer2, self.artwork1.ledger)

    def test_remove_from_art_collection(self):
        """Test case for the remove_from_art_collection method of the Peer class."""

        self.peer.remove_from_art_collection(self.artwork1)
        self.assertNotIn(self.artwork1, self.peer.art_collection.artworks)

    def test_swap_art(self):
        """Test case for the swap_art method of the Peer class."""

        self.peer.art_collection.add_to_art_collection(self.artwork1)
        self.peer2.art_collection.add_to_art_collection(self.artwork2)
        self.peer.swap_art(self.artwork1, self.artwork2, self.peer2)
        self.assertNotIn(self.artwork1, self.peer.art_collection.artworks)
        self.assertIn(self.artwork2, self.peer.art_collection.artworks)
        self.assertNotIn(self.artwork2, self.peer2.art_collection.artworks)
        self.assertIn(self.artwork1, self.peer2.art_collection.artworks)


if __name__ == "__main__":
    # Create an event loop
    loop = asyncio.get_event_loop()

    # Run the tests and await the results
    async def run_tests():
        """Run the tests."""
        await unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))

    result = loop.run_until_complete(run_tests())
    # Close the event loop
    loop.close()
