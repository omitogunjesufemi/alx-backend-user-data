#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if type(authorization_header) != str:
            return None

        starts_with_basic = authorization_header.startswith("Basic ")
        if starts_with_basic:
            return authorization_header.split("Basic ")[1]
        else:
            return None
