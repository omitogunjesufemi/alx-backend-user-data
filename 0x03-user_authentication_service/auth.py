#!/usr/bin/env python3
"""
This module is for authentication methods
"""
import bcrypt
from db import DB
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """ """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise(ValueError(f"User {email} already exists"))
        except NoResultFound:
            hsh_pwd = _hash_password(password)
            return self._db.add_user(email, hsh_pwd)


def _hash_password(password: str) -> bytes:
    """
    Takes a string argument and return bytes which is a salted hash
    of the input password
    """
    password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
