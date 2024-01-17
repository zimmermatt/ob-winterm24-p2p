#!/usr/bin/env python3
"""
Test Module for the Peer class
"""

import time
import unittest
from unittest.mock import Mock, patch
from threading import Timer
from peer.peer import Peer


class TestPeer(unittest.TestCase):
    """
    Class to test peer functionality.
    """

    def setUp(self):
        """
        Initialize IPFS Mock and Peer instance
        """
        self.mock_ipfs = Mock()
        self.peer = Peer("127.0.0.1", 5001, self.mock_ipfs)

    def test_initialization(self):
        """
        Test case to verify the initialization of the Peer class.
        """
        # Verify that the network address is set to "127.0.0.1"
        self.assertEqual(self.peer.network_address, "127.0.0.1")
        # Verify that the port is set to 5001
        self.assertEqual(self.peer.port, 5001)
        # Verify that the IPFS instance is set to the mock_ipfs object
        self.assertEqual(self.peer.ipfs, self.mock_ipfs)

    def test_connect(self):
        """
        Test case for connecting to the network.
        """
        self.mock_ipfs.connect.return_value = True
        result = self.peer.connect_to_network()
        self.assertTrue(result)
        self.mock_ipfs.connect.assert_called_once()

    @patch("builtins.input", side_effect=["10", "20", "10"])
    @patch(
        "threading.Timer",
        side_effect=lambda delay, func, args: Timer(0.001, func, args),
    )
    def test_commission_art_piece(self, mock_input, mock_timer):
        """
        Test case for the commission_art_piece method of the Peer class.
        This test verifies that the commission_art_piece method correctly adds a commission,
        publishes it on IPFS, and schedules and sends a deadline notice.
        """
        print(mock_input, mock_timer)
        self.peer.commission_art_piece()
        self.assertEqual(len(self.peer.commissions), 1)
        commission = self.peer.commissions[0]
        self.assertEqual(commission.width, 10)
        self.assertEqual(commission.height, 20)
        self.assertEqual(commission.wait_time, 10)
        self.mock_ipfs.ipfs_publish.assert_called_once_with(
            "placeholder_ipfs_file_descriptor", commission
        )
        time.sleep(0.02)
        # Check that send_deadline_reached was called, which in turn calls ipfs_publish
        self.mock_ipfs.ipfs_publish.assert_called_with(
            commission.get_file_descriptor(), "Commission complete"
        )


if __name__ == "__main__":
    unittest.main()
