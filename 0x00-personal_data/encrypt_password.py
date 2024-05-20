#!/usr/bin/env python3
"""
A module that hashes a password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a string into a password
    """
    password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
