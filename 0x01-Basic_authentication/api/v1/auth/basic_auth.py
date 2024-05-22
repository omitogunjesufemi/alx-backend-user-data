#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string:
        - base64_authorization_header
        """
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) != str:
            return None

        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_value.decode("utf-8")
            return decoded_value
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        email, password = None, None

        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        else:
            splitted_values = decoded_base64_authorization_header.split(":", 1)
            email, password = splitted_values[0], splitted_values[1]

        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the user email and password.
        """
        if (user_email is None) or (type(user_email) != str):
            return None

        if (user_pwd is None) or (type(user_pwd) != str):
            return None

        db_list = User.all()
        if len(db_list) == 0:
            return None

        attr = {"email": user_email}
        user_list = User.search(attr)

        if (len(user_list) == 0) or user_list is None:
            return None

        user = user_list[0]
        if user.email != user_email:
            return None

        if user.is_valid_password(user_pwd) is False:
            return None

        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Overloads Auth and retrieves the User instance for a request
        """
        auth_header = super().authorization_header(request)

        ex_b64_hr = None
        if auth_header:
            ex_b64_hr = self.extract_base64_authorization_header(auth_header)
        else:
            return None

        decoded_b64_hr = None
        if ex_b64_hr:
            decoded_b64_hr = self.decode_base64_authorization_header(ex_b64_hr)
        else:
            return None

        usr_cred = None
        if decoded_b64_hr:
            usr_cred = self.extract_user_credentials(decoded_b64_hr)
        else:
            return None

        usr_email = usr_cred[0]
        usr_pwd = usr_cred[1]

        user = self.user_object_from_credentials(usr_email, usr_pwd)

        if user is None:
            return None

        return user
