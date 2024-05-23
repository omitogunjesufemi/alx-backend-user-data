#!/usr/bin/env python3
"""
This module contains the SessionAuth class that inherits from Auth
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Class SessionAuth that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for user_id
        """
        if user_id is None:
            return None

        if type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None

        if type(session_id) != str:
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> TypeVar("User"):
        """
        (Overload) Returns a User instance based on a cookie value
        """
        if request is None:
            return None

        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)

        user = User.get(user_id)
        return user
