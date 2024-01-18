#!/usr/bin/env python3

"""
Simple Test Module for the Artwork class
"""

import unittest
from commission.artwork import Artwork


class TestArtwork(unittest.TestCase):
    """Test class for Artwork class"""

    def setUp(self):
        """Create an instance of Artwork with width=10, height=20, and wait_time=0.5"""
        self.artwork = Artwork(10, 20, 0.5)

    def test_initialization(self):
        """Check if the attributes are initialized correctly"""
        self.assertEqual(self.artwork.width, 10)
        self.assertEqual(self.artwork.height, 20)
        self.assertEqual(self.artwork.get_wait_time(), 0.5)
        self.assertEqual(self.artwork.commission_complete, False)

    def test_generate_key(self):
        """Test the generate_file_descriptor method of Artwork"""
        descriptor = self.artwork.generate_key()
        # Assuming the descriptor should be a string
        self.assertIsInstance(descriptor, str)


if __name__ == "__main__":
    unittest.main()
