#!/usr/bin/env python3
"""Module for testing the Ledger class"""

import unittest
from unittest.mock import MagicMock
from ledger.ledger import Ledger


class TestLedger(unittest.TestCase):
    """
    Test class for Ledger class
    """

    def setUp(self):
        self.ledger = Ledger()
        self.mock_peer1 = MagicMock()
        self.mock_peer1.keys = {"public": "public_key1"}
        self.mock_peer2 = MagicMock()
        self.mock_peer2.keys = {"public": "public_key2"}

    def test_add_owner(self):
        """
        Test the add_owner method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.assertEqual(self.ledger.stack[-1][0], self.mock_peer1)

    def test_verify_integrity(self):
        """
        Test the verify_integrity method of Ledger
        """

        self.ledger.add_owner(self.mock_peer1)
        self.assertTrue(self.ledger.verify_integrity())

        self.ledger.add_owner(self.mock_peer2)
        self.assertTrue(self.ledger.verify_integrity())

        self.ledger.stack[0] = (self.mock_peer1, b"corrupted_hash")
        self.assertFalse(self.ledger.verify_integrity())


if __name__ == "__main__":
    unittest.main()
