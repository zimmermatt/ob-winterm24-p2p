"""
Module to manage art collections for Art Collectors.
"""

from commission.artwork import Artwork


class ArtCollection:
    """
    Class to manage art collections for Art Collectors
    """

    def __init__(self) -> None:
        """
        Initialize the art collection by creating an empty list for the artworks
        in the collection
        """

        self.artworks = set()

    def add_to_art_collection(self, artwork: Artwork):
        """
        Add an artwork to the collection
        """

        self.artworks.add(artwork)

    def remove_from_art_collection(self, artwork: Artwork):
        """
        Remove an artwork from the collection
        """

        self.artworks.discard(artwork)
