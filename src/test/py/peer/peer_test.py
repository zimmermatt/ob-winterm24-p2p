#!/usr/bin/env python3
"""
Test Module for the Peer class
"""

import asyncio
from collections import namedtuple, deque
from datetime import timedelta
import logging
import pickle
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
        self.mock_node = AsyncMock(
            spec=MockNode,
            node=namedtuple(
                "MockChildNode", ["long_id"], defaults=(int(hex(12345), 16),) * 1
            ),
        )
        self.mock_kdm.return_value = self.mock_node
        self.peer = Peer(
            5001,
            "src/test/py/resources/peer_test",
            "127.0.0.1:5000",
            self.mock_kdm,
        )

        self.peer.logger = MagicMock()

        self.deadline_task = None
        self.peer.ledger = Ledger()
        self.artwork1 = Artwork(10, 10, timedelta(minutes=10), self.peer.ledger)
        self.artwork2 = Artwork(10, 10, timedelta(minutes=10), self.peer.ledger)

        self.peer.inventory = Inventory()
        self.peer.inventory.add_owned_artwork(self.artwork1)
        self.peer.node = self.mock_node
        self.peer.wallet = Wallet()

        self.peer2 = Peer(
            8000, "src/test/py/resources/peer_test", "127.0.0.1:5000", self.mock_kdm
        )

        self.offer_announcement_trade = OfferAnnouncement(
            self.artwork1, 0, "trade", "public_key"
        )
        self.offer_announcement_sale = OfferAnnouncement(
            self.artwork1, 10, "sale", "public_key"
        )
        self.offer_response_trade = OfferResponse(
            "exchange_id", self.artwork1, 0, "trade", "public_key"
        )
        self.offer_response_sale = OfferResponse(
            "exchange_id", self.artwork1, 10, "sale", "public_key"
        )

        self.trade_type = "trade"
        self.sale_type = "sale"
        self.announcement_key = "announcement_key"
        self.exchange_key = "exchange_key"

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

    @patch("builtins.input", side_effect=["10", "20", "5", "10"])
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
            self.assertEqual(commission.constraint.palette_limit, 5)
            self.assertLessEqual(commission.wait_time, timedelta(seconds=10))
            await self.deadline_task

    def test_add_owner(self):
        """
        Test the add_owner method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        self.assertEqual(self.peer.ledger.queue[-1][0], self.peer.keys["public"])

    def test_get_owner(self):
        """
        Test the get_owner method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        self.assertEqual(self.peer.ledger.get_owner(), self.peer.keys["public"])

    def test_get_previous_owner(self):
        """
        Test the get_previous_owner method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        self.assertIsNone(self.peer.ledger.get_previous_owner())

        self.peer.ledger.add_owner(self.peer2.keys["public"])
        self.assertEqual(
            self.peer.ledger.get_previous_owner(), self.peer.keys["public"]
        )

    def test_get_originator(self):
        """
        Test the get_originator method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        self.assertEqual(self.peer.ledger.get_originator(), self.peer.keys["public"])

    def test_get_owner_history(self):
        """
        Test the get_owner_history method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        expected_queue = deque([(self.peer.keys["public"], self.peer.ledger.top)])
        self.assertEqual(self.peer.ledger.get_owner_history(), expected_queue)

    def test_verify_integrity(self):
        """
        Test the verify_integrity method of Ledger
        """

        self.peer.ledger.add_owner(self.peer.keys["public"])
        self.assertTrue(self.peer.ledger.verify_integrity())

        self.peer.ledger.add_owner(self.peer2.keys["public"])
        self.assertTrue(self.peer.ledger.verify_integrity())

        self.peer.ledger.queue[0] = (self.peer, b"corrupted_hash")
        self.assertFalse(self.peer.ledger.verify_integrity())

    async def test_handle_exchange_announcement_deadline(self):
        """
        Test for the handle_exchange_announcement_deadline method of the Peer class.
        """

        self.peer.inventory.add_pending_exchange(
            self.announcement_key, self.offer_announcement_sale
        )

        await self.peer.handle_exchange_announcement_deadline(
            self.sale_type, self.announcement_key, self.offer_announcement_sale
        )

        self.assertNotIn(self.announcement_key, self.peer.inventory.pending_exchanges)
        self.assertIn(self.announcement_key, self.peer.inventory.completed_exchanges)
        self.assertEqual(10, self.peer.wallet.get_balance())
        self.peer.logger.info.assert_any_call("Exchange announcement deadline reached")
        self.peer.node.set.assert_called_once_with(
            self.announcement_key, pickle.dumps(self.offer_announcement_sale)
        )
        self.peer.logger.info.assert_any_call("%s announced", self.sale_type)

    async def test_announce_exchange(self):
        """
        Test for the announce_exchange method of the Peer class.
        """

        await self.peer.announce_exchange(self.trade_type, 0, timedelta(seconds=10))

        self.peer.logger.info.assert_any_call("Announcing exchange")
        self.assertEqual(1, len(self.peer.inventory.pending_exchanges))
        self.peer.node.set.assert_called_once()
        self.peer.logger.info.assert_any_call("%s announced", self.trade_type)

        self.peer.inventory.remove_owned_artwork(self.artwork1)
        self.assertEqual(0, len(self.peer.inventory.owned_artworks))
        await self.peer.announce_exchange(self.trade_type, 0, timedelta(seconds=10))
        self.peer.logger.info.assert_any_call("No artwork for exchange")

    async def test_announce_exchange_fail(self):
        """
        Test for the announce_exchange method of the Peer class for an invalid
        exchange type.
        """

        await self.peer.announce_exchange("invalid", 0, timedelta(seconds=10))
        self.peer.logger.error.assert_any_call("Invalid exchange type")
        self.peer.inventory.remove_owned_artwork(self.artwork1)

    async def test_send_exchange_response_trade(self):
        """
        Test for the send_exchange_response method of the Peer class for trade.
        """

        await self.peer.send_exchange_response(
            self.exchange_key, self.offer_announcement_trade
        )
        self.peer.logger.info.assert_any_call(
            "Sending %s response to %s",
            self.offer_announcement_trade.get_exchange_type(),
            self.offer_announcement_trade.get_originator_public_key(),
        )

        self.peer.node.set.assert_called_once()
        self.peer.logger.info.assert_any_call(
            "%s response sent", self.offer_announcement_trade.get_exchange_type()
        )

        self.peer.inventory.remove_owned_artwork(self.artwork1)
        self.assertEqual(0, len(self.peer.inventory.owned_artworks))
        await self.peer.send_exchange_response(
            self.exchange_key, self.offer_announcement_trade
        )
        self.peer.logger.info.assert_any_call("No artwork to send")

    async def test_send_exchange_response_sale(self):
        """
        Test for the send_exchange_response method of the Peer class for sale.
        """

        await self.peer.send_exchange_response(
            self.exchange_key, self.offer_announcement_sale
        )
        self.peer.logger.info.assert_any_call("Insufficient funds.")

        self.peer.wallet.add_to_balance(10)
        await self.peer.send_exchange_response(
            self.exchange_key, self.offer_announcement_sale
        )

        self.peer.logger.info.assert_any_call(
            "Sending %s response to %s",
            self.offer_announcement_sale.get_exchange_type(),
            self.offer_announcement_sale.get_originator_public_key(),
        )

        self.peer.node.set.assert_called_once()
        self.peer.logger.info.assert_any_call(
            "%s response sent", self.offer_announcement_sale.get_exchange_type()
        )

    async def test_handle_exchange_response_success(self):
        """
        Test for the handle_exchange_response method of the Peer class for success case.
        """

        self.peer.inventory.add_pending_exchange(
            self.exchange_key, self.offer_response_sale
        )

        self.peer.wallet.add_to_balance(10)
        await self.peer.handle_exchange_response(
            self.exchange_key, self.offer_response_sale
        )

        self.peer.logger.info.assert_any_call("Handling exchange response")
        self.assertEqual(0, len(self.peer.inventory.pending_exchanges))
        self.assertEqual(0, self.peer.wallet.get_balance())

        self.peer.logger.info(
            "%s accepted the exchange.",
            self.offer_response_sale.get_exchanger_public_key,
        )

        self.peer.logger.info("Exchange successful")
        self.assertEqual(
            self.offer_response_sale.get_exchanger_public_key(),
            self.peer.ledger.get_owner(),
        )

    async def test_handle_exchange_response_fail(self):
        """
        Test for the handle_exchange_response method of the Peer class for failure case.
        """

        await self.peer.handle_exchange_response(
            self.exchange_key, self.offer_response_sale
        )
        self.peer.logger.info.assert_any_call("Handling exchange response")
        self.peer.logger.info(
            "%s rejected the exchange.",
            self.offer_response_sale.get_exchanger_public_key,
        )
        self.peer.logger.info("Exchange unsuccessful")

    # def test_commission_with_palette_limit:


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
