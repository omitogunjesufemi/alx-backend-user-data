#!/usr/bin/env python3
"""
This module is for authentication methods
"""
import bcrypt
import uuid
from db import DB
from user import User
from typing import TypeVar, Optional
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise(ValueError(f"User {email} already exists"))
        except NoResultFound:
            hsh_pwd = _hash_password(password)
            return self._db.add_user(email, hsh_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Locate user by email and check if password matches"""
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            password = password.encode("utf-8")
            if bcrypt.checkpw(password, hashed_pwd):
                return True
            return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Return a string representation of a new UUID"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Find user corresponding to the email and generate a new
        UUID and store it in the database as the user's session_id

        Return the Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self,
                                 session_id: str) -> Optional[User]:
        """Returns user from session_id"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the user's session ID to None"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_rest_password_token(self, email: str) -> str:
        """Find the user corresponing to the email and generate a UUID
        and update the user's reset token database field

        If the user does not exist, raise ValueError

        Return the token"""
        pass


def _hash_password(password: str) -> bytes:
    """
    Takes a string argument and return bytes which is a salted hash
    of the input password
    """
    password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
