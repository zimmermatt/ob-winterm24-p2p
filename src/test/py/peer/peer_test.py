#!/usr/bin/env python3
"""
Test Module for the Peer class
"""

import asyncio
from datetime import timedelta
import logging
import pickle
from collections import deque
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from commission.artwork import Artwork
from peer.peer import Peer
from peer.ledger import Ledger
from peer.inventory import Inventory
from peer.wallet import Wallet


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

        self.peer.logger = MagicMock()

        self.deadline_task = None
        self.ledger = Ledger()
        self.artwork1 = Artwork(10, 10, timedelta(minutes=10), self.ledger)
        self.artwork2 = Artwork(10, 10, timedelta(minutes=10), self.ledger)

        self.peer.inventory = Inventory()
        self.peer.inventory.add_owned_artwork(self.artwork1)
        self.peer.node = self.mock_node
        self.peer.wallet = Wallet()
        self.peer.wallet.add_to_balance(20)

        self.peer2 = Peer(
            8000, "src/test/py/resources/peer_test", "127.0.0.1:5000", self.mock_kdm
        )

        # self.trade_key = b"trade_key"
        # self.response = OfferResponse(self.trade_key, "artwork_id", "public_key")

        self.artwork_price = 10

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

    def test_get_owner(self):
        """
        Test the get_owner method of Ledger
        """

        self.ledger.add_owner(self.peer)
        self.assertEqual(self.ledger.get_owner(), self.peer.keys["public"])

    def test_get_previous_owner(self):
        """
        Test the get_previous_owner method of Ledger
        """

        self.ledger.add_owner(self.peer)
        self.assertIsNone(self.ledger.get_previous_owner())

        self.ledger.add_owner(self.peer2)
        self.assertEqual(self.ledger.get_previous_owner(), self.peer.keys["public"])

    def test_get_originator(self):
        """
        Test the get_originator method of Ledger
        """

        self.ledger.add_owner(self.peer)
        self.assertEqual(self.ledger.get_originator(), self.peer.keys["public"])

    def test_get_owner_history(self):
        """
        Test the get_owner_history method of Ledger
        """

        self.ledger.add_owner(self.peer)
        expected_queue = deque([(self.peer.keys["public"], self.ledger.top)])
        self.assertEqual(self.ledger.get_owner_history(), expected_queue)

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

    # async def test_announce_trade(self):
    #     """
    #     Test the announce_trade method of the Peer class.
    #     """

    #     await self.peer.announce_trade()

    #     self.assertEqual(len(self.peer.inventory.pending_trades), 1)

    #     self.peer.logger.info.assert_has_calls(
    #         [call("Announcing trade"), call("Trade announced")]
    #     )

    #     self.peer.node.set = MagicMock(return_value=False)
    #     await self.peer.announce_trade()

    #     self.peer.logger.error.assert_called_once_with("Trade type is not pickleable")

    # async def test_send_trade_response(self):
    #     """
    #     Test case for the send_trade_response method of the Peer class.
    #     """

    #     announcement = OfferAnnouncement(
    #         originator_public_key="originator_public_key",
    #         artwork_id="artwork_id",
    #     )

    #     await self.peer.send_trade_response(self.trade_key, announcement)

    #     self.mock_node.set.assert_called_once()

    #     _, response_value = self.mock_node.set.call_args[0]

    #     response = pickle.loads(response_value)
    #     self.assertIsInstance(response, OfferResponse)
    #     self.assertEqual(response.trade_id, self.trade_key)

    #     self.assertIn(response.artwork_id, self.peer.inventory.owned_artworks)

    #     self.assertEqual(response.originator_public_key, self.peer.keys["public"])

    #     self.peer.logger.info.assert_any_call(
    #         "Sending trade response to %s", announcement.originator_public_key
    #     )
    #     self.peer.logger.info.assert_any_call("Trade response sent")

    # async def test_handle_trade_response_success(self):
    #     """
    #     Test case for the handle_trade_response method of the Peer class for success case.
    #     """

    #     self.peer.inventory.pending_trades = {self.trade_key: "trade_value"}
    #     await self.peer.handle_trade_response(self.trade_key, self.response)
    #     self.peer.logger.info.assert_any_call(self.response)
    #     self.peer.logger.info.assert_any_call("Trade successful")
    #     self.assertNotIn(self.trade_key, self.peer.inventory.pending_trades)

    # async def test_handle_trade_response_fails(self):
    #     """
    #     Test case for the handle_trade_response method of the Peer class for failure case.
    #     """

    #     self.peer.inventory.pending_trades = {}
    #     await self.peer.handle_trade_response(self.trade_key, self.response)
    #     self.peer.logger.info.assert_any_call("Trade unsuccessful")


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
