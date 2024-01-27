#!/usr/bin/env python3
"""Test module for ArtCollection class"""

import unittest
from datetime import timedelta
from commission.artwork import Artwork
from commission.artcollection import ArtCollection
from ledger.ledger import Ledger


class TestArtCollection(unittest.TestCase):
    """
    Test class for ArtCollection class
    """

    def setUp(self):
        """
        Initialize ArtCollection instance, Ledger instance, and Artwork instances
        """

        self.ledger = Ledger()
        self.artwork1 = Artwork(10, 10, timedelta(minutes=10), self.ledger)
        self.artwork2 = Artwork(10, 10, timedelta(minutes=10), self.ledger)
        self.collection = ArtCollection()

    def test_add_to_art_collection(self):
        """
        Test the add_to_art_collection method of ArtCollection
        This verifies that the add_to_art_collection method correctly adds an
        """

        self.collection.add_to_art_collection(self.artwork1)
        self.assertIn(self.artwork1, self.collection.artworks)

    def test_remove_from_art_collection(self):
        """
        Test the remove_from_art_collection method of ArtCollection
        This verifies that the remove_from_art_collection method correctly removes an
        """

        self.collection.add_to_art_collection(self.artwork1)
        self.collection.remove_from_art_collection(self.artwork1)
        self.assertNotIn(self.artwork1, self.collection.artworks)


if __name__ == "__main__":
    unittest.main()
