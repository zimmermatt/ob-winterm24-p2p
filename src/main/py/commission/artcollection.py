"""
Module to manage art collections for Art Collectors.
"""

from commission.artwork import Artwork


class ArtCollection:
    """
    Class to manage art collections for Art Collectors
    """

    def __init__(self) -> None:
        self.artworks = []

    def get_artworks(self):
        """
        Returns the artworks in the collection
        """

        return self.artworks

    def add_to_art_collection(self, artwork: Artwork):
        """
        Add an artwork to the collection
        """

        self.artworks.append(artwork)
        # add new owner to ledger

    def remove_from_art_collection(self, artwork: Artwork):
        """
        Remove an artwork from the collection
        """

        self.artworks.remove(artwork)
        # garbage collect previous owner?
