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
        Defining Routes that don't need authentication
        """
        if path is None:
            return True

        if (excluded_paths is None) or (len(excluded_paths) == 0):
            return True

        if path in excluded_paths:
            return False

        slash_tolerant = path.endswith("/")
        if slash_tolerant is False:
            new_path = path + "/"
            if new_path in excluded_paths:
                return False
            else:
                return True

        return True

    def authorization_header(self, request=None) -> str:
        """
        Validate all request to secure the API

        request - Flask request object
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return: None

        request - Flask request object
        """
        return None
