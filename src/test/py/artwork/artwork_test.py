#!/usr/bin/env python3

"""
Simple Test Module for the Artwork class
"""

from datetime import timedelta
import unittest
from unittest.mock import Mock
from commission.artwork import Artwork


class TestArtwork(unittest.TestCase):
    """Test class for Artwork class"""

    def setUp(self):
        """Create an instance of Artwork with width=10, height=20, and wait_time=0.5"""
        mock_ledger = Mock()
        self.artwork = Artwork(10, 20, timedelta(seconds=0.5), mock_ledger)

    def test_initialization(self):
        """Check if the attributes are initialized correctly"""
        self.assertEqual(self.artwork.width, 10)
        self.assertEqual(self.artwork.height, 20)
        self.assertLessEqual(self.artwork.get_remaining_time(), 0.5)
        self.assertEqual(self.artwork.commission_complete, False)

    def test_generate_key(self):
        """Test the generate_file_descriptor method of Artwork"""
        descriptor = self.artwork.generate_key()
        self.assertIsInstance(descriptor, bytes)


if __name__ == "__main__":
    unittest.main()
