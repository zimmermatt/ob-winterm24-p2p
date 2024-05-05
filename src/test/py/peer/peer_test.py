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
from exchange.offer_announcement import OfferAnnouncement
from exchange.offer_response import OfferResponse


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


# pylint: disable=too-many-public-methods
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

    async def test_handle_exchange_announcement_deadline_trade(self):
        """
        Test case for the handle_exchange_announcement_deadline method for the trade exchange_type
        of the Peer class.
        """

        announcement_type = "trade"
        announcement_key = "key"
        offer_announcement = OfferAnnouncement("trade", 0, "artwork")

        await self.peer.handle_exchange_announcement_deadline(
            announcement_type, announcement_key, offer_announcement
        )

        self.assertNotIn(announcement_key, self.peer.inventory.pending_exchanges)
        self.assertIn(announcement_key, self.peer.inventory.completed_exchanges)
        self.peer.node.set.assert_called_once_with(
            announcement_key, pickle.dumps(offer_announcement)
        )
        self.peer.logger.info.assert_any_call("Exchange announcement deadline reached")
        self.peer.logger.info.assert_any_call("%s announced", announcement_type)

    async def test_handle_exchange_announcement_deadline_sale(self):
        """
        Test case for the handle_exchange_announcement_deadline method for the sale exchange type
        of the Peer class.
        """

        announcement_type = "trade"
        announcement_key = "key"
        offer_announcement = OfferAnnouncement("trade", 10, "artwork")

        await self.peer.handle_exchange_announcement_deadline(
            announcement_type, announcement_key, offer_announcement
        )

        self.assertNotIn(announcement_key, self.peer.inventory.pending_exchanges)
        self.assertIn(announcement_key, self.peer.inventory.completed_exchanges)
        self.assertEqual(self.peer.wallet.get_balance(), 30)
        self.peer.node.set.assert_called_once_with(
            announcement_key, pickle.dumps(offer_announcement)
        )
        self.peer.logger.info.assert_any_call("Exchange announcement deadline reached")
        self.peer.logger.info.assert_any_call("%s announced", announcement_type)

    async def test_handle_exchange_announcement_deadline_failure(self):
        """
        Test case for the handle_exchange_announcement_deadline method for the failure case
        """

        announcement_type = "invalid"
        announcement_key = "key"
        offer_announcement = OfferAnnouncement("trade", 0, "artwork")

        self.peer.node.set = AsyncMock(side_effect=TypeError())

        await self.peer.handle_exchange_announcement_deadline(
            announcement_type, announcement_key, offer_announcement
        )

        self.peer.logger.error.assert_called_with(
            "%s type is not pickleable", announcement_type
        )

    async def test_announce_exchange_trade(self):
        """
        Test case for the announce_exchange method of the Peer class for trade exchange type.
        """

        self.mock_node.set = AsyncMock(return_value=True)
        self.peer.inventory.get_artwork_to_exchange = MagicMock(
            return_value=self.artwork1
        )
        self.peer.handle_exchange_announcement_deadline = AsyncMock()

        await self.peer.announce_exchange("trade", 10, timedelta(seconds=20))

        self.peer.logger.info.assert_any_call("Announcing exchange")
        self.peer.inventory.get_artwork_to_exchange.assert_called_once()
        self.mock_node.set.assert_called_once()
        self.peer.handle_exchange_announcement_deadline.assert_called_once()

    async def test_announce_exchange_sale(self):
        """
        Test case for the announce_exchange method of the Peer class for sale exchange type.
        """

        self.mock_node.set = AsyncMock(return_value=True)
        self.peer.inventory.get_artwork_to_exchange = MagicMock(
            return_value=self.artwork1
        )
        self.peer.handle_exchange_announcement_deadline = AsyncMock()

        await self.peer.announce_exchange("sale", 10, timedelta(seconds=20))

        self.peer.logger.info.assert_any_call("Announcing exchange")
        self.peer.inventory.get_artwork_to_exchange.assert_called_once()
        self.mock_node.set.assert_called_once()
        self.peer.handle_exchange_announcement_deadline.assert_called_once()

    async def test_announce_exchange_invalid_exchange_type(self):
        """
        Test case for the announce_exchange method of the Peer class for invalid
        exchange type.
        """

        await self.peer.announce_exchange("invalid", 10, timedelta(seconds=20))

        self.peer.logger.error.assert_called_once_with("Invalid exchange type")

    async def send_exchange_response_trade(self):
        """
        Test case for the send_exchange_response method of the Peer class for trade exchange type.
        """

        exchange_key = b"key"
        offer_announcement = OfferAnnouncement("trade", 0, "artwork", "public_key")
        artwork_to_exchange = self.artwork1

        self.peer.keys["public"] = "public_key"
        self.peer.inventory.artworks = [artwork_to_exchange]

        await self.peer.send_exchange_response(exchange_key, offer_announcement)

        self.peer.logger.info.assert_called_with(
            "Sending %s response to %s", "trade", "public_key"
        )

        self.assertIn(exchange_key, self.peer.inventory.pending_exchanges)
        self.peer.node.set.assert_called_once()
        self.peer.logger.info.assert_called_with("%s response sent", "trade")

    async def send_exchange_response_sale(self):
        """
        Test case for the send_exchange_response method of the Peer class for sale exchange type.
        """

        exchange_key = b"key"
        offer_announcement = OfferAnnouncement("sale", 10, "artwork", "public_key")
        artwork_to_exchange = self.artwork1

        self.peer.keys["public"] = "public_key"
        self.peer.inventory.artworks = [artwork_to_exchange]

        await self.peer.send_exchange_response(exchange_key, offer_announcement)

        self.peer.logger.info.assert_called_with(
            "Sending %s response to %s", "sale", "public_key"
        )

        self.assertIn(exchange_key, self.peer.inventory.pending_exchanges)
        self.peer.node.set.assert_called_once()
        self.peer.logger.info.assert_called_with("%s response sent", "sale")

    async def test_handle_exchange_response_trade(self):
        """
        Test case for the handle_exchange_response method of the Peer class for
        trade exchange type.
        """

        self.peer.handle_accept_exchange = AsyncMock()
        self.peer.handle_reject_exchange = AsyncMock()

        exchange_key = b"key"
        response = OfferResponse("trade", "artwork", 0, "public_key")
        self.peer.inventory.pending_exchanges = {exchange_key: "value"}

        await self.peer.handle_exchange_response(exchange_key, response)

        self.peer.logger.info.assert_any_call("Handling exchange response")
        self.assertNotIn(exchange_key, self.peer.inventory.pending_exchanges)
        self.peer.handle_accept_exchange.assert_called_once_with(response)
        self.peer.logger.info.assert_any_call("Exchange successful")
        self.peer.handle_reject_exchange.assert_not_called()

    async def test_handle_exchange_response_sale(self):
        """
        Test case for the handle_exchange_response method of the Peer class for
        sale exchange type.
        """

        self.peer.handle_accept_exchange = AsyncMock()
        self.peer.handle_reject_exchange = AsyncMock()

        exchange_key = b"key"
        response = OfferResponse("sale", "artwork", 10, "public_key")
        self.peer.inventory.pending_exchanges = {exchange_key: "value"}

        await self.peer.handle_exchange_response(exchange_key, response)

        self.peer.logger.info.assert_any_call("Handling exchange response")
        self.assertNotIn(exchange_key, self.peer.inventory.pending_exchanges)
        self.peer.handle_accept_exchange.assert_called_once_with(response)
        self.peer.logger.info.assert_any_call("Exchange successful")
        self.peer.handle_reject_exchange.assert_not_called()

    async def test_handle_exchange_response_failure(self):
        """
        Test case for the handle_exchange_response method of the Peer class for failure case.
        """

        exchange_key = b"key"
        response = OfferResponse("trade", "artwork", 0, "public_key")
        self.peer.inventory.pending_exchanges = {}

        await self.peer.handle_exchange_response(exchange_key, response)

        self.peer.logger.info.assert_any_call("Handling exchange response")
        self.peer.logger.info.assert_any_call("Exchange unsuccessful")

    async def test_handle_accept_exchange(self):
        """Test case for the handle_accept_exchange method of the Peer class."""

        response = OfferResponse("sale", "artwork", 10, "public_key")

        await self.peer.handle_accept_exchange(response)

        self.assertEqual(10, self.peer.wallet.get_balance())
        self.peer.logger.info.assert_called_once_with(
            "%s accepted the exchange.", response.get_originator_public_key()
        )

    async def test_handle_reject_exchange(self):
        """Test case for the handle_reject_exchange method of the Peer class."""

        response = OfferResponse("sale", "artwork", 10, "public_key")

        await self.peer.handle_reject_exchange(response)

        self.peer.logger.info.assert_called_once_with(
            "%s rejected the exchange.", response.get_originator_public_key()
        )


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
