#!/usr/bin/env python3
"""
SessionDB Authentication Module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Class SessionDBAuth authentication class that inherits from
    SessionExpAuth
    """
    def create_session(self, user_id=None):
        """ Creates and store new instance of UserSession
        - Returns the Session ID
        """
        session_id = super().create_session(user_id)
        print(f"Session ID: {session_id}")
        if session_id is None:
            return None

        usr_attr = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**usr_attr)
        if not user_session:
            return None

        user_session.save()
        print(f"User Session: {user_session}")
        print(f"User Session: {user_session.user_id}")
        print(f"User Session: {user_session.session_id}")
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the DB
        based on session_id
        """
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None

        user_session_list = UserSession.search({'session_id': session_id})
        if len(user_session_list) == 0:
            return None

        user_session = user_session_list[0]
        if not user_session:
            return None

        if user_session.user_id != user_id:
            return None

        return user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from
        the request cookie
        """
        if request is None:
            return False

        cookie = self.session_cookie(request)
        if not cookie:
            return False

        user_id = self.user_id_for_session_id(cookie)
        if not user_id:
            return False

        user_session_list = UserSession.search({'session_id': cookie})
        if len(user_session_list) == 0:
            return None

        user_session = user_session_list[0]
        if not user_session:
            return None

        if user_session.user_id != user_id:
            return None

        user_session.remove()
        return True
