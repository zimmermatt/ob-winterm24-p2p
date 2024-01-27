"""Module for testing the Ledger class"""

import unittest
from unittest.mock import MagicMock
from peer.peer import Peer
from ledger.ledger import Ledger


class TestLedger(unittest.TestCase):
    """
    Test class for Ledger class
    """

    def setUp(self):
        self.ledger = Ledger()
        self.mock_peer1 = MagicMock(spec=Peer)
        self.mock_peer1.keys = {"public": "public_key1"}
        self.mock_peer2 = MagicMock(spec=Peer)
        self.mock_peer2.keys = {"public": "public_key2"}

    def test_add_owner(self):
        """
        Test the add_owner method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.assertEqual(self.ledger.get_current_owner(), self.mock_peer1)

    def test_get_current_version(self):
        """
        Test the get_current_version method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.assertIsNotNone(self.ledger.get_current_version())

    def test_get_specified_version(self):
        """
        Test the get_specified_version method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.ledger.add_owner(self.mock_peer2)
        self.assertIsNotNone(self.ledger.get_specified_version(0))
        self.assertIsNotNone(self.ledger.get_specified_version(1))

    def test_get_specified_owner(self):
        """
        Test the get_specified_owner method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.ledger.add_owner(self.mock_peer2)
        self.assertEqual(self.ledger.get_specified_owner(0), self.mock_peer1)
        self.assertEqual(self.ledger.get_specified_owner(1), self.mock_peer2)

    def test_get_history(self):
        """
        Test the get_history method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.ledger.add_owner(self.mock_peer2)
        self.assertEqual(len(self.ledger.get_history()), 2)

    def test_verify_integrity(self):
        """
        Test the verify_integrity method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.assertTrue(self.ledger.verify_integrity())

        self.ledger.add_owner(self.mock_peer2)
        self.assertTrue(self.ledger.verify_integrity())

        # Corrupt the ledger by changing a hash
        self.ledger.stack[0] = (self.mock_peer1, b"corrupted_hash")
        self.assertFalse(self.ledger.verify_integrity())


if __name__ == "__main__":
    unittest.main()
