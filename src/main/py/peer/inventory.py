#!/usr/bin/env python3
"""
Module to manage peer inventory functionality.

The Inventory class keeps track of our commissions, owned artworks, and artworks pending exchange.
"""
import random
from commission.artwork import Artwork


class Inventory:
    """Class to manage Peer artwork inventory"""

    def __init__(self) -> None:
        """Initializes an instance of the Inventory class"""
        self.commissions = {}
        self.owned_artworks = {}
        self.pending_exchanges = {}
        self.artworks_pending_exchange = set()
        self.completed_exchanges = set()
        self.commission_canvases = {}

    def add_commission(self, artwork: Artwork):
        """
        Adds a commission to the inventory.

        Params:
        - artwork (Artwork): The artwork to add to the inventory.
        """

        self.commissions[artwork.key] = artwork

    def add_owned_artwork(self, artwork: Artwork):
        """
        Adds an owned artwork to the inventory.

        Params:
        - artwork (Artwork): The artwork to add to the inventory.
        """

        self.owned_artworks[artwork.key] = artwork

    def add_pending_exchange(self, exchange_key, exchange_offer):
        """
        Adds an artwork pending exchange to the inventory.

        Params:
        - exchange_key (bytes): The key of the artwork to add to the inventory.
        - exchange_offer (OfferAnnouncement | OfferResponse): The exchange offer
        to add to the inventory.
        """

        self.artworks_pending_exchange.add(exchange_offer.artwork)
        self.pending_exchanges[exchange_key] = exchange_offer

    def remove_commission(self, artwork: Artwork):
        """
        Removes a commission from the inventory.

        Params:
        - artwork (Artwork): The artwork to remove from the inventory.
        """

        if artwork.key in self.commissions:
            del self.commissions[artwork.key]

    def remove_owned_artwork(self, artwork: Artwork):
        """
        Removes an owned artwork from the inventory.

        Params:
        - artwork (Artwork): The artwork to remove from the inventory.
        """

        if artwork.key in self.owned_artworks:
            del self.owned_artworks[artwork.key]

    def remove_pending_exchange(self, exchange_key):
        """
        Removes an artwork pending exchange from the inventory.

        Params:
        - artwork (Artwork): The artwork to remove from the inventory.
        """

        if exchange_key in self.pending_exchanges:
            del self.pending_exchanges[exchange_key]

    def get_commission(self, key: bytes):
        """
        Returns a commission from the inventory.

        Params:
        - key (bytes): The key of the commission to get from the inventory.
        """

        if key in self.commissions:
            return self.commissions[key]
        raise KeyError(f"No commission found for key: {key}")

    def get_owned_artwork(self, key: bytes):
        """
        Returns an owned artwork from the inventory.

        Params:
        - key (bytes): The key of the owned artwork to get from the inventory.
        """

        if key in self.owned_artworks:
            return self.owned_artworks[key]
        raise KeyError(f"No owned artwork found for key: {key}")

    def is_owned_artwork(self, key: bytes):
        """
        Returns whether or not an artwork is owned.

        Params:
        - key (bytes): The key of the artwork to check.
        """

        return key in self.owned_artworks

    def get_artwork_to_exchange(self):
        """
        Gets a random artwork to exchange from the inventory.
        """

        available_artworks = [
            artwork
            for artwork in self.owned_artworks.values()
            if artwork.key not in self.artworks_pending_exchange
        ]
        if len(available_artworks) > 0:
            random_artwork = random.choice(available_artworks)
            return random_artwork
        return None

    def get_artwork_by_id(self, artwork_id: bytes):
        """
        Returns an owned artwork from the inventory by its ID.
        """

        for artwork in self.owned_artworks.values():
            if artwork.id == artwork_id:
                return artwork
        raise KeyError(f"No owned artwork found for ID: {artwork_id}")
