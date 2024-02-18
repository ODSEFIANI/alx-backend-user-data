#!/usr/bin/env python3
"""
Authentication module
"""
from typing import (
    List,
    TypeVar
)
from flask import request


class Auth:
    """
    Authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks for authenticaion requirement
        Args:
            - path(str): Url path of the requested page
            - excluded_paths(List of str): List of paths contents
              that require authentication
        Return:
            - Flase if path is in excluded_paths, else True
        """

        if excluded_paths is None or excluded_paths == []:
            return True
        elif path is None:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returne
        """
        return None

    def session_cookie(self, request=None):
        """
        SEnd a cookie to the client Browser
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
