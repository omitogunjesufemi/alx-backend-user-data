#!/usr/bin/env python3
"""
This module contains the Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class Auth: template for all authentication system to be implemented
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return: False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Return: None

        request - Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return: None

        request - Flask request object
        """
        return None
