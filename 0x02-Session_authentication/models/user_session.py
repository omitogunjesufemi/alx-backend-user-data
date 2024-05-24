#!/usr/bin/env python3
"""
A module that contains the class UserSession
"""
from models.base import Base


class UserSession(Base):
    """
    Class UserSession
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initialization
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
