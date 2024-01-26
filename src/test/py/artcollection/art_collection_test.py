"""Test module for ArtCollection class"""

import unittest
from datetime import timedelta
from commission.artcollection import ArtCollection
from commission.artwork import Artwork


class TestArtCollection(unittest.TestCase):
    """
    Test class for ArtCollection class
    """

    def setUp(self):
        """
        Create an instance of ArtCollection and Artwork
        with width=100, height=100, and wait_time=1 day
        """

        self.collection = ArtCollection()
        self.artwork1 = Artwork(100.0, 100.0, timedelta(days=1))
        self.artwork2 = Artwork(200.0, 200.0, timedelta(days=2))

    def test_add_to_art_collection(self):
        """
        Test the add_to_art_collection method of ArtCollection
        This test verifies that the add_to_art_collection method correctly
        """

        self.collection.add_to_art_collection(self.artwork1)
        self.assertIn(self.artwork1, self.collection.get_artworks())

    def test_remove_from_art_collection(self):
        """Test the remove_from_art_collection method of ArtCollection
        This test verifies that the remove_from_art_collection method correctly
        and removes an artwork from a collection
        """

        self.collection.add_to_art_collection(self.artwork1)
        self.collection.remove_from_art_collection(self.artwork1)
        self.assertNotIn(self.artwork1, self.collection.get_artworks())


if __name__ == "__main__":
    unittest.main()
