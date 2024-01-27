#!/usr/bin/env python3
"""
Module to manage some utils used accross the project
"""

import hashlib
import random
import string


def generate_random_sha1_hash():
    """
    Generates a random SHA-1 hash as a file descriptor for the trade response.
    """
    key_length = 10
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(key_length))
    sha1_hash = hashlib.sha1(random_string.encode()).digest()
    return sha1_hash
