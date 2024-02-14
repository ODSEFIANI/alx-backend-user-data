#!/usr/bin/env python3
"""
BasicAuth clss module
"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ basic authentc
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        retrieve relevant information containg Basic
        Authorization
        """

        if not isinstance(authorization_header, str):
            return None
        if authorization_header is None:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        head_info = authorization_header.split(" ")[-1]
        return head_info

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decrypth a Base64-encrypted header string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decrypted = base64_authorization_header.encode('utf-8')
            decrypted = base64.b64decode(decrypted)
            return decrypted.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns authentication info user email
        and pswd
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        u_email = decoded_base64_authorization_header.split(":")[0]
        u_password = decoded_base64_authorization_header.split(":")[1]
        return (u_email, u_password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Return a User iwith that credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User object to authenticate with
        """
        header_auth = self.authorization_header(request)
        if header_auth is not None:
            token = self.extract_base64_authorization_header(header_auth)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return
