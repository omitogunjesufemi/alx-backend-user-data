#!/usr/bin/env python3
"""
Session Authentication with an expiration date
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime
from datetime import timedelta


class SessionExpAuth(SessionAuth):
    """
    Class SessionExpAuth that inherits from SessionAuth
    """
    def __init__(self):
        """Setting the Session Duration
        """
        try:
            duration = int(getenv("SESSION_DURATION"))
            self.session_duration = duration
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creating a session id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {}
        user_id = self.user_id_by_session_id[session_id]
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user ID from session dictionary
        """
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not self.user_id_by_session_id.get(session_id):
            return None

        session_duration = self.session_duration
        user_id = session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        datetime_add = created_at + timedelta(seconds=session_duration)
        if datetime_add < datetime.now():
            return None

        return user_id
