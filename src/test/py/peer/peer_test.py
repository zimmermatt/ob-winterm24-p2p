#!/usr/bin/env python3
"""
Test Module for the Peer class
"""

import asyncio
from datetime import timedelta
import logging
import pickle
import unittest
from unittest.mock import patch, call, MagicMock, AsyncMock
from commission.artwork import Artwork
from peer.peer import Peer
from peer.ledger import Ledger
from peer.inventory import Inventory
from trade.offer_announcement import OfferAnnouncement
from trade.offer_response import OfferResponse


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
        self.mock_kdm.return_value = self.mock_node
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
        self.ledger = Ledger()
        self.peer.keys = {"public": "public_key1"}
        self.peer2.keys = {"public": "public_key2"}

        self.peer.logger = MagicMock()
        self.peer.logger.info = MagicMock()

        self.peer.inventory = Inventory()
        self.peer.inventory.add_owned_artwork(self.artwork1)
        self.peer.inventory.add_owned_artwork(self.artwork2)

        self.peer.inventory.remove_pending_trade = MagicMock()

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

    def test_add_owner(self):
        """
        Test the add_owner method of Ledger
        """

        self.ledger.add_owner(self.peer)
        self.assertEqual(self.ledger.queue[-1][0], self.peer.keys["public"])

    def test_verify_integrity(self):
        """
        Test the verify_integrity method of Ledger
        """

        self.ledger.add_owner(self.peer)
        self.assertTrue(self.ledger.verify_integrity())

        self.ledger.add_owner(self.peer2)
        self.assertTrue(self.ledger.verify_integrity())

        self.ledger.queue[0] = (self.peer, b"corrupted_hash")
        self.assertFalse(self.ledger.verify_integrity())

    async def test_announce_trade(self):
        """
        Test the announce_trade method of the Peer class.
        """

        self.peer.node = self.mock_node
        self.peer.logger.info.reset_mock()

        await self.peer.announce_trade()

        self.assertEqual(len(self.peer.inventory.pending_trades), 1)

        self.assertEqual(self.peer.logger.info.call_count, 2)
        self.assertEqual(
            self.peer.logger.info.call_args_list[0], call("Announcing trade")
        )
        self.assertEqual(
            self.peer.logger.info.call_args_list[1], call("Trade announced")
        )

    async def test_send_trade_response(self):
        """
        Test case for the send_trade_response method of the Peer class.
        """

        self.peer.node = self.mock_node
        trade_key = b"trade_key"
        announcement = OfferAnnouncement(
            originator_public_key="originator_public_key",
            artwork_ledger_key="artwork_ledger_key",
        )

        await self.peer.send_trade_response(trade_key, announcement)

        self.mock_node.set.assert_called_once()

        _, response_value = self.mock_node.set.call_args[0]

        response = pickle.loads(response_value)
        self.assertIsInstance(response, OfferResponse)
        self.assertEqual(response.trade_id, trade_key)

        self.assertIn(response.artwork_ledger_key, self.peer.inventory.owned_artworks)

        self.assertEqual(response.originator_public_key, self.peer.keys["public"])

    async def test_handle_trade_response(self):
        """
        Test case for the handle_trade_response method of the Peer class.
        """
        trade_key = b"trade_key"
        response = OfferResponse(trade_key, "artwork_ledger_key", "public_key")

        self.peer.inventory.pending_trades = {trade_key: "trade_value"}
        with patch.object(self.peer.logger, "info") as mock_info:
            await self.peer.handle_trade_response(trade_key, response)
            self.peer.inventory.remove_pending_trade.assert_called_with(trade_key)
            mock_info.assert_any_call(response)
            mock_info.assert_any_call("Trade successful")

        self.peer.inventory.pending_trades = {}
        with patch.object(self.peer.logger, "info") as mock_info:
            await self.peer.handle_trade_response(trade_key, response)
            mock_info.assert_any_call(response)
            mock_info.assert_any_call("Trade unsuccessful")


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
